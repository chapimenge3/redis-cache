import time
import requests
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from faker import Faker

from quiz.models import Options, Question, Quiz


fake = Faker()
User = get_user_model()

URL = 'https://opentdb.com/api.php?amount=25'


class Command(BaseCommand):
    help = "create fake quiz"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def get_quiz(self):
        c = 0
        while c < 5:
            response = requests.get(URL)
            if response.status_code == 200:
                return response.json()['results']
            else:
                self.stdout.write(self.style.HTTP_INFO(
                    f'Response code is {response.status_code}'))
                self.stdout.write(self.style.HTTP_INFO(
                    f'Response data is {response.json()}'))
                self.stdout.write(self.style.HTTP_INFO('Waiting for 3 sec'))
                time.sleep(3)
                c += 1

    def handle(self, *args, **options):
        total = options.get('count', 10)
        users = User.objects.all()
        for i in range(total):
            with transaction.atomic():
                title = " ".join(fake.sentence().split()[:10])
                quiz = Quiz(title=title, is_published=True,
                            created_by=random.choice(users))
                quiz.save()
                questions = self.get_quiz()
                questions_list = []
                for q in questions:
                    question = Question(
                        question_type=q['type'], question=q['question'])
                    question.save()
                    options_list = []
                    for op in q['incorrect_answers']:
                        option = Options(option=op)
                        option.save()
                        options_list.append(option)

                    option = Options(
                        option=q['correct_answer'], is_correct=True)
                    option.save()
                    options_list.append(option)
                    question.options.add(*options_list)
                    questions_list.append(question)

                quiz.questions.add(*questions_list)
                self.stdout.write(self.style.SUCCESS(f'Created {i+1} quiz'))
