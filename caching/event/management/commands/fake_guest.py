from django.core.management.base import BaseCommand, CommandError
from event.models import Event, Guest
from random import choice
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'create fake new guest'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        total = options['count']
        events = Event.objects.all()
        for i in range(total):
            Guest.objects.create(
                name=fake.name(),
                event=choice(events),
                email=fake.email(),
            )
            self.stdout.write(self.style.SUCCESS(f'Created {i+1} guest'))

        self.stdout.write(self.style.SUCCESS('______________________________'))
        self.stdout.write(self.style.SUCCESS(f'Created {total} guest'))
