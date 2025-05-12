from rest_framework import viewsets, permissions
from rest_framework.response import Response
from utils import apply_search_filter, apply_date_filter
from .models import Exercise, ExerciseItem
from .serializers import (
    ExerciseSerializer,
    ExerciseListSerializer,
    ExerciseItemSerializer,
    ExerciseItemCreateSerializer
)

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Exercise.objects.all()
        return apply_search_filter(self.request, queryset, fields=['name', 'type'])

    def get_serializer_class(self):
        if self.action == 'list':
            return ExerciseListSerializer
        return ExerciseSerializer

class ExerciseItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseItemSerializer
    
    def get_queryset(self):
        queryset = ExerciseItem.objects.filter(user=self.request.user)
        return apply_date_filter(self.request, queryset)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExerciseItemCreateSerializer
        return ExerciseItemSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 