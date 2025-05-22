from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from .models import UserPlan, PlanItem
from datetime import timedelta


class UserPlanModelUnitTests(TestCase):
    def test_default_start_end_dates(self):
        user = User.objects.create_user('pu', 'pu@example.com', 'pass')
        plan = UserPlan.objects.create(
            user=user, initial_weight=60.0, goal_weight=55.0,
            calorie_intake_goal=1800, exercise_calorie_goal=400
        )
        self.assertEqual(plan.start_date, plan.start_date)
        self.assertEqual(plan.end_date, plan.start_date + timedelta(days=30))

class PlanItemModelUnitTests(TestCase):
    def test_unique_together_constraint(self):
        user = User.objects.create_user('pu2', 'pu2@example.com', 'pass')
        plan = UserPlan.objects.create(
            user=user, initial_weight=60, goal_weight=55,
            calorie_intake_goal=1800, exercise_calorie_goal=400
        )
        PlanItem.objects.create(plan=plan, date='2023-01-04')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            PlanItem.objects.create(plan=plan, date='2023-01-04')

class PlansIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('pi', 'pi@example.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_only_one_active_plan(self):
        url = reverse('plan-list')

        resp1 = self.client.post(url, {
            'initial_weight': 70, 'goal_weight': 65,
            'calorie_intake_goal': 2000, 'exercise_calorie_goal': 500
        }, format='json')
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)

        resp2 = self.client.post(url, {
            'initial_weight': 72, 'goal_weight': 68,
            'calorie_intake_goal': 1800, 'exercise_calorie_goal': 300
        }, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)

        active = self.client.get(url + '?is_active=true')
        self.assertEqual(len(active.data), 1)
        self.assertEqual(active.data[0]['id'], resp2.data['id'])