import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from quiz.models import QuizResult, Quiz

User = get_user_model()


class Command(BaseCommand):
    help = "create fake quiz result"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        total = options.get('count', 10)
        users = User.objects.all()
        quizs = Quiz.objects.all()
        for _ in range(total):
            QuizResult.objects.create(
                quiz=random.choice(quizs),
                user=random.choice(users),
                score=random.randint(0, 100),
            )
            self.stdout.write(self.style.SUCCESS(f'Created {_+1} Quiz Result'))
