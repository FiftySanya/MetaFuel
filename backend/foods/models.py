from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    fiber = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    allergens = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Сніданок'),
        ('lunch', 'Обід'),
        ('dinner', 'Вечеря'),
        ('snack', 'Перекус'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.user.username}'s {self.get_meal_type_display()} on {self.date}"
    
    class Meta:
        unique_together = ['user', 'meal_type', 'date']
        ordering = ['date', 'meal_type']

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount in grams")
    
    def __str__(self):
        return f"{self.amount}g of {self.product.name}"
    
    @property
    def calories(self):
        return round((self.product.calories * self.amount) / 100, 1)
    
    @property
    def protein(self):
        return round((self.product.protein * self.amount) / 100, 1)
    
    @property
    def fat(self):
        return round((self.product.fat * self.amount) / 100, 1)
    
    @property
    def carbs(self):
        return round((self.product.carbs * self.amount) / 100, 1) 