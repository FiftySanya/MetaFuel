from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ExerciseItemViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'exercise-items', ExerciseItemViewSet, basename='exerciseitem')

urlpatterns = [
    path('', include(router.urls)),
] 