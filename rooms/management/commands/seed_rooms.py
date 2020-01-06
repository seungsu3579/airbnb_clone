import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_model
from users import models as user_model

class Command(BaseCommand):

    help = 'This Command creates Fake Rooms.'

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="How many users do you want to create")

    def handle(self, *args, **options):    
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_model.User.objects.all()
        room_types = room_model.RoomType.objects.all()
        seeder.add_entity(room_model.Room, number, {
            'name': lambda x : seeder.faker.address(),
            'host': lambda x : random.choice(all_users),
            'room_type': lambda x : random.choice(room_types),
            'price' : lambda x : random.randint(30, 300),
            'guests' : lambda x : random.randint(1, 15),
            'beds' : lambda x : random.randint(1, 5),
            'bedrooms' : lambda x : random.randint(1, 5),
            'baths' : lambda x : random.randint(1, 5),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} Fake Rooms Created!'))
