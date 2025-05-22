from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from django.test import TestCase
from .views import UserViewSet
from .serializers import UserSerializer


class UserSerializerUnitTests(TestCase):
    def test_user_serializer_fields(self):
        user = User(username='user1', email='user1@example.com')
        data = UserSerializer(user).data
        self.assertEqual(set(data.keys()), {'username', 'email'})
        self.assertEqual(data['username'], 'user1')
        self.assertEqual(data['email'], 'user1@example.com')

class UserViewUnitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='pass', email='u2@example.com')
        self.factory = APIRequestFactory()

    def test_me_action_returns_user_data(self):
        view = UserViewSet.as_view({'get': 'me'})
        request = self.factory.get('/api/users/me/')
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'username': self.user.username, 'email': self.user.email})

class UsersIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user3', password='pass', email='u3@example.com')
        self.client = APIClient()

    def test_me_endpoint_flow(self):
        resp = self.client.get('/api/users/me/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        resp = self.client.get('/api/users/me/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], self.user.username)
        self.assertEqual(resp.data['email'], self.user.email)
