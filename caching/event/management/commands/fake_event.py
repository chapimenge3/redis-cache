from django.core.management.base import BaseCommand, CommandError
from event.models import Event

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'create fake new events'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        total = options['count']
        for i in range(total):
            Event.objects.create(
                name=fake.name(),
                date=fake.date_time(),
                location=fake.address(),
                description=fake.text(),
            )
            self.stdout.write(self.style.SUCCESS(f'Created {i+1} events'))

        self.stdout.write(self.style.SUCCESS('______________________________'))
        self.stdout.write(self.style.SUCCESS(f'Created {total} events'))
