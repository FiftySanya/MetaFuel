from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from utils import apply_search_filter, apply_date_filter
from .models import Product, Meal, MealItem
from .serializers import (ProductSerializer, ProductListSerializer, MealSerializer, MealItemCreateSerializer)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        return apply_search_filter(self.request, queryset, fields=['name'])

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

class MealViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MealSerializer
    
    def get_queryset(self):
        return apply_date_filter(self.request, Meal.objects.filter(user=self.request.user))
    
    def create(self, request, *args, **kwargs):
        serializer = MealSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        meal, created = Meal.objects.get_or_create(
            user=request.user,
            meal_type=data['meal_type'],
            date=data['date']
        )
        resp = MealSerializer(meal)
        return Response(resp.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        meal = self.get_object()
        serializer = MealItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        meal_item = serializer.save(meal=meal)
        data = MealSerializer(meal).data
        data['calculated'] = {
            'calories': meal_item.calories,
            'protein': meal_item.protein,
            'fat': meal_item.fat,
            'carbs': meal_item.carbs
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        meal = self.get_object()
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({'error': 'item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        item = get_object_or_404(MealItem, pk=item_id, meal=meal)
        item.delete()
        return Response(MealSerializer(meal).data, status=status.HTTP_200_OK) 