from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Product, Meal, MealItem


class ProductModelUnitTests(TestCase):
    def test_str_and_fields(self):
        p = Product.objects.create(name='P', calories=100, protein=5, fat=2, carbs=20)
        self.assertEqual(str(p), 'P')
        self.assertEqual(p.calories, 100)

class MealItemModelUnitTests(TestCase):
    def test_calories_property(self):
        u = User.objects.create_user('fu', 'fu@example.com', 'pass')
        prod = Product.objects.create(name='Apple', calories=52, protein=0.3, fat=0.2, carbs=14)
        meal = Meal.objects.create(user=u, meal_type='lunch', date='2023-01-01')
        mi = MealItem.objects.create(meal=meal, product=prod, amount=200)
        expected = round((52 * 200) / 100, 1)
        self.assertEqual(mi.calories, expected)

class FoodsIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('fi', 'fi@example.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.product = Product.objects.create(name='B', calories=80, protein=1, fat=0.5, carbs=18)

    def test_create_meal_add_and_remove_item(self):
        meal_url = reverse('meal-list')
        resp = self.client.post(meal_url, {'meal_type': 'breakfast', 'date': '2023-01-03'}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED))
        meal_id = resp.data['id']

        add_url = reverse('meal-add-item', args=[meal_id])
        resp = self.client.post(add_url, {'product': self.product.id, 'amount': 50}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('calculated', resp.data)

        item_id = resp.data['items'][0]['id']
        remove_url = reverse('meal-remove-item', args=[meal_id])
        resp = self.client.delete(remove_url, {'item_id': item_id}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['items'], [])