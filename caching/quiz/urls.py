from rest_framework.routers import DefaultRouter

from quiz import views

router = DefaultRouter()
router.register(r'quiz', views.QuizView, basename='quiz')
router.register(r'quiz-result', views.QuizView, basename='quiz-result')

urlpatterns = router.urls
