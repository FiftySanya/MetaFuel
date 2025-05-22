from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Exercise, ExerciseItem
from django.test import TestCase
from rest_framework.reverse import reverse
from .serializers import ExerciseListSerializer


class ExerciseModelUnitTests(TestCase):
    def test_calories_burned_property(self):
        exercise = Exercise.objects.create(
            name='Test', type='силова', duration=40,
            intensity='низька', calories_burned=120
        )

        item = ExerciseItem.objects.create(
            user=User.objects.create_user('u', 'p'), 
            exercise=exercise, date='2023-01-01', duration=20
        )
        expected = int(120 * (20 / 40))
        self.assertEqual(item.calories_burned, expected)

class ExerciseSerializerUnitTests(TestCase):
    def test_list_serializer_fields(self):
        ex = Exercise(name='X', type='аеробна', duration=10, intensity='висока', calories_burned=50)
        data = ExerciseListSerializer(ex).data
        self.assertEqual(set(data.keys()), {'id', 'name', 'duration', 'calories_burned'})

class ExercisesIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('int_u', 'int@example.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.exercise = Exercise.objects.create(
            name='Run', type='аеробна', duration=30,
            intensity='середня', calories_burned=150
        )

    def test_list_and_create_exercise_item(self):
        list_url = reverse('exercise-list')
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(resp.data, list))

        create_url = reverse('exerciseitem-list')
        resp = self.client.post(create_url, {
            'exercise': self.exercise.id,
            'date': '2023-01-02',
            'duration': 15
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(resp.data.keys()), {'exercise', 'date', 'duration'})

        list_items_url = reverse('exerciseitem-list')
        resp2 = self.client.get(list_items_url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        items = resp2.data
        self.assertTrue(isinstance(items, list) and len(items) == 1)
        item = items[0]
        self.assertIn('id', item)
        self.assertIn('calories_burned', item)
        expected = int(self.exercise.calories_burned * (15 / self.exercise.duration))
        self.assertEqual(item['calories_burned'], expected)
