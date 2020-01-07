import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_model
from users import models as user_model
from rooms import models as room_model

class Command(BaseCommand):

    help = 'This Command creates Fake Lists.'

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="How many users do you want to create")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_model.User.objects.all()

        seeder.add_entity(list_model.List, number, {
            'user': lambda x: random.choice(users),
        })

        created_lists = seeder.execute()
        clean_lists = flatten(list(created_lists.values()))
        rooms = room_model.Room.objects.all()
        for pk in clean_lists:
            choosed_list = list_model.List.objects.get(pk=pk)
            for i in range(random.randint(2,20)):
                choosed_list.rooms.add(random.choice(rooms))

        self.stdout.write(self.style.SUCCESS(f'{number} Fake Lists Created!'))

