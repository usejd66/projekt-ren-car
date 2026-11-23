from django.core.management.base import BaseCommand

from car_app.images import make_variants
from car_app.models import Car


class Command(BaseCommand):
    help = "Krijon versionet WebP (480/960/1600 px) për fotot e makinave që nuk i kanë ende."

    def handle(self, *args, **options):
        created = 0
        for car in Car.objects.exclude(image=""):
            try:
                n = make_variants(car.image.name)
            except (OSError, ValueError) as exc:
                self.stderr.write(f"{car}: {exc}")
                continue
            created += n
            self.stdout.write(f"{car}: {n} version(e) të reja")
        self.stdout.write(self.style.SUCCESS(f"Gati: {created} versione të krijuara."))
