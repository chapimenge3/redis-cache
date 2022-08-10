from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

QUESTION_TYPE = (
    ('multiple', 'multiple'),
    ('boolean', 'boolean')
)

class Options(models.Model):
    option = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option

class Question(models.Model):
    question = models.CharField(max_length=200)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    options = models.ManyToManyField(Options)

    def __str__(self):
        return self.question

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.quiz.title
