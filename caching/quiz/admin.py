from django.contrib import admin

from quiz.models import Options, Question, Quiz, QuizResult

for i in [Options, Question, Quiz, QuizResult]:
    admin.site.register(i)
