from datetime import timedelta

from django.contrib import admin, messages
from django.utils import timezone

from . import emails
from . import stats
from .models import Car, CarPhoto, ContactMessage, Lead, Reservation, Review, Subscriber


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 1
    fields = ("image", "order")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "transmission", "fuel", "seats", "price_per_day", "is_available", "is_featured")
    list_filter = ("category", "transmission", "fuel", "is_available", "is_featured")
    list_editable = ("price_per_day", "is_available", "is_featured")
    search_fields = ("brand", "name")
    inlines = [CarPhotoInline]
    view_on_site = True


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "car", "pickup_date", "return_date", "total_price", "status", "cancel_request", "created_at")
    list_filter = ("status", ("cancel_requested_at", admin.EmptyFieldListFilter), "car", "pickup_date")
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("total_price", "created_at", "cancel_requested_at")

    @admin.display(description="Kërkesë anulimi", boolean=True)
    def cancel_request(self, obj):
        return bool(obj.cancel_requested_at) and obj.status != "cancelled"
    date_hierarchy = "pickup_date"
    actions = ["confirm_reservations", "cancel_reservations"]

    @admin.action(description="Konfirmo rezervimet e zgjedhura (dhe njofto klientët me email)")
    def confirm_reservations(self, request, queryset):
        # Një rezervim i anuluar mund të mbivendoset me një tjetër aktiv: mos e konfirmo atë.
        skipped, done = [], 0
        for r in queryset.exclude(status="confirmed"):
            if r.status == "cancelled" and Reservation.overlapping(
                r.car_id, r.pickup_date, r.return_date, r.pk
            ).exists():
                skipped.append(f"#{r.pk}")
                continue
            Reservation.objects.filter(pk=r.pk).update(status="confirmed")
            r.status = "confirmed"
            emails.booking_status_changed(r)
            done += 1
        if done:
            self.message_user(request, f"{done} rezervim(e) u konfirmuan; klientët u njoftuan me email.")
        if skipped:
            self.message_user(
                request,
                "Nuk u konfirmuan (makina është e zënë në ato data): " + ", ".join(skipped),
                level=messages.WARNING,
            )

    @admin.action(description="Anulo rezervimet e zgjedhura (dhe njofto klientët me email)")
    def cancel_reservations(self, request, queryset):
        done = 0
        for r in queryset.exclude(status="cancelled"):
            Reservation.objects.filter(pk=r.pk).update(status="cancelled")
            r.status = "cancelled"
            emails.booking_status_changed(r)
            done += 1
        if done:
            self.message_user(request, f"{done} rezervim(e) u anuluan; klientët u njoftuan me email.")

    def save_model(self, request, obj, form, change):
        # statusi u ndryshua nga faqja e rezervimit te admin: njofto klientin
        status_changed = change and "status" in form.changed_data
        super().save_model(request, obj, form, change)
        if status_changed:
            emails.booking_status_changed(obj)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    list_editable = ("is_approved",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("email",)
    date_hierarchy = "subscribed_at"

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Rezultatet: sa rezervime dhe kontakte solli faqja, dhe nga cilat kanale."""

    change_list_template = "admin/car_app/lead/results.html"
    list_display = ("created_at", "kind", "source", "page", "reservation")
    list_filter = ("kind", "source", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False  # krijohen automatikisht nga faqja

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        today = timezone.localdate()
        period = request.GET.get("period", "this")
        if period == "last":
            start, end = stats.previous_month(today)
        elif period == "30":
            start, end = today - timedelta(days=29), today + timedelta(days=1)
        else:
            period = "this"
            start, end = stats.month_range(today)
        # "period" nuk është fushë e modelit: hiqe para se ta shohë lista e Django-s
        if "period" in request.GET:
            request.GET = request.GET.copy()
            request.GET.pop("period")
        extra_context = {
            **(extra_context or {}),
            "period": period,
            "summary": stats.period_stats(start, end),
            "months": stats.last_months(6, today),
        }
        return super().changelist_view(request, extra_context=extra_context)
