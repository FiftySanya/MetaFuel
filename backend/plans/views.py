from rest_framework import viewsets, permissions
from .models import UserPlan, PlanItem
from .serializers import UserPlanSerializer, PlanItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from utils import apply_date_filter, apply_bool_filter


class UserPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPlanSerializer

    def get_queryset(self):
        qs = UserPlan.objects.filter(user=self.request.user)
        return apply_bool_filter(self.request, qs, 'is_active')

    def perform_create(self, serializer):
        with transaction.atomic():
            UserPlan.objects.filter(user=self.request.user, is_active=True).update(is_active=False)
            serializer.save(user=self.request.user, is_active=True)

    @action(detail=True, methods=['get'])
    def daily_metrics(self, request, pk=None):
        plan = self.get_object()
        days = plan.days.order_by('date')
        serializer = PlanItemSerializer(days, many=True)
        return Response(serializer.data)

class PlanItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlanItemSerializer

    def get_queryset(self):
        queryset = PlanItem.objects.filter(plan__user=self.request.user)
        plan_param = self.request.query_params.get('plan')
        if plan_param:
            try:
                queryset = queryset.filter(plan__id=int(plan_param))
            except ValueError:
                pass
        else:
            queryset = queryset.filter(plan__is_active=True)
            
        return apply_date_filter(self.request, queryset)
