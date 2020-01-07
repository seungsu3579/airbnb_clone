import random
from django.contrib.admin.utils import flatten
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
        
        # strong Entity
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

        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = room_model.Amenity.objects.all()
        facilities = room_model.Facility.objects.all()
        rules = room_model.HouseRule.objects.all()

        for pk in created_clean:
            created_room = room_model.Room.objects.get(pk=pk)

            # ForeignKey
            for i in range(random.randint(5,10)):
                room_model.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=created_room,
                    file=f'room_photos/{random.randint(1,31)}.webp',
                )
                seeder.add_entity(room_model.Photo, 1,{
                    'caption': seeder.faker.sentence(),
                    'file': f'room_photos/{random.randint(1,31)}.webp',
                    'room': created_room,
                })


            # Many To Many
            for a in amenities:
                if random.randint(0,1) == 1:
                    created_room.amenities.add(a)

            for f in facilities:
                if random.randint(0,2) == 1:
                    created_room.facilities.add(f)

            for r in rules:
                if random.randint(0,1) == 1:
                    created_room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f'{number} Fake Rooms Created!'))
