from dataclasses import field
from rest_framework import serializers

from quiz.models import Options, Question, Quiz, QuizResult

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ('id', 'option')
        read_only_fields = ('id',)

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id', 'question', 'options', 'question_type')
        read_only_fields = ('id',)

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'questions', 'is_published', 'created_at')
        read_only_fields = ('id',)

class QuizResultSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    class Meta:
        model = QuizResult
        fields = ('id', 'quiz', 'score')
        read_only_fields = ('id',)