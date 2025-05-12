from rest_framework import serializers
from .models import Product, Meal, MealItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'calories', 'protein', 'fat', 'carbs', 'fiber', 'sugar', 'sodium', 'allergens']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'calories']

class MealItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    calories = serializers.ReadOnlyField()
    protein = serializers.ReadOnlyField()
    fat = serializers.ReadOnlyField()
    carbs = serializers.ReadOnlyField()
    
    class Meta:
        model = MealItem
        fields = ['id', 'product_details', 'amount', 'calories', 'protein', 'fat', 'carbs']

class MealItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ['product', 'amount'] 

class MealSerializer(serializers.ModelSerializer):
    items = MealItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'date', 'items']
        read_only_fields = ['id']