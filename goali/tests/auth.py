from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils import timezone
from goali.models import Goal


class TokenTests(APITestCase):
    def auth_helper(self):
        self.user = User.objects.create_user(username="stephen", password="12345678")
        url = "/login/"
        data = {
            "username": "stephen",
            "password": "12345678",
        }
        response = self.client.post(url, data, format='json')
        return response.data['token']

    def setup_goal(self):
        set_up_url = "/goals/"
        set_up_data = {
            "name": "New goal",
            "description": "describe this",
            "completed": "false",
        }
        set_up_response = self.auth_client.post(set_up_url, set_up_data, format='json')
        self.assertEqual(set_up_response.status_code, status.HTTP_201_CREATED)
        return set_up_response.data['id']

    def test_get_goals_with_expired_token(self):
        key = self.auth_helper()
        token = Token.objects.get(key=key)
        expired = timezone.make_aware(
            datetime(
                token.created.year,
                token.created.month,
                token.created.day - 1,
                token.created.hour - 1,
                token.created.minute,
                token.created.second
            )
        )
        Token.objects.update(created=expired)
        self.auth_client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key) 
        url = "/goals/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Token.objects.count(), 0)

