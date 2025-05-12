from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserPlanViewSet, PlanItemViewSet

router = DefaultRouter()
router.register(r'plans', UserPlanViewSet, basename='plan')
router.register(r'days', PlanItemViewSet, basename='planitem')

urlpatterns = [
    path('', include(router.urls)),
] 