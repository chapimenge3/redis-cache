from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from quiz.serializers import QuizSerializer, QuizResultSerializer
from quiz.models import Quiz, QuizResult

CACHE_TTL = 60 * 15
USE_CACHE = False
INVALIDATE_CACHE = False
USE_IMPROVED_Query = False


class QuizView(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = Quiz.objects

        if USE_IMPROVED_Query:
            query = query.prefetch_related(
                'questions', 'questions__options')

        result = query.all()
        return result

    def get_object(self):
        query = self.filter_queryset(self.get_queryset())
        pk = self.kwargs['pk']
        try:
            if USE_IMPROVED_Query:
                query = query.prefetch_related(
                    'questions', 'questions__options')

            query = query.get(pk=pk)
            return query
        except Quiz.DoesNotExist:
            raise Quiz.DoesNotExist("Quiz Doesn't exist")

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class QuizResultView(viewsets.ModelViewSet):
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = QuizResultSerializer.objects

        result = query.all()

        return result

    def get_object(self):
        query = self.filter_queryset(self.get_queryset())
        pk = self.kwargs['pk']
        try:
            query = query.get(pk=pk, user=self.request.user)
            return query
        except QuizResult.DoesNotExist:
            raise QuizResult.DoesNotExist("Quiz result Doesn't exist")

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
