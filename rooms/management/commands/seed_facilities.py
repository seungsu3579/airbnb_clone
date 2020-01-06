from django.core.management.base import BaseCommand
from rooms.models import Facility

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        help = 'This Command creates Facilities.'

        facilities = [
            "private entrance",
            "paid parking on premises",
            "paid parkinig off premises",
            "elevator",
            "parking",
            "gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f'{len(facilities)} Facilities Created!'))
