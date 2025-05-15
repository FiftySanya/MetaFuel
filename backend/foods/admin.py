from django.contrib import admin
from .models import Product, Meal, MealItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'calories', 'protein', 'fat', 'carbs', 'fiber', 'sugar', 'sodium')
    search_fields = ('name',)
    list_filter = ('calories',)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'meal_type', 'date')
    list_filter = ('meal_type', 'date', 'user')
    search_fields = ('user__username',)

@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal', 'product', 'amount')
    list_filter = ('meal__meal_type', 'meal__date')
    search_fields = ('meal__user__username', 'product__name') 