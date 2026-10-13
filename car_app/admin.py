from django.contrib import admin

from .models import Car, ContactMessage, Reservation, Review, Subscriber


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "transmission", "fuel", "seats", "price_per_day", "is_available", "is_featured")
    list_filter = ("category", "transmission", "fuel", "is_available", "is_featured")
    list_editable = ("price_per_day", "is_available", "is_featured")
    search_fields = ("brand", "name")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "car", "pickup_date", "return_date", "total_price", "status", "created_at")
    list_filter = ("status", "car", "pickup_date")
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("total_price", "created_at")
    date_hierarchy = "pickup_date"
    actions = ["confirm_reservations", "cancel_reservations"]

    @admin.action(description="Konfirmo rezervimet e zgjedhura")
    def confirm_reservations(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="Anulo rezervimet e zgjedhura")
    def cancel_reservations(self, request, queryset):
        queryset.update(status="cancelled")


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