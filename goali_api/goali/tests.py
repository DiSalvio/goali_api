from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from goali.models import Goal

class GoalTests(APITestCase):
    def auth_helper(self):
        self.user = User.objects.create_user("stephen", "stephen@disalv.io", "12345678")
        url = "/api/login"
        data = {
            "username": "stephen",
            "password": "12345678",
        }
        response = self.client.post(url, data, format='json')
        self.auth_client = APIClient(HTTP_AUTHORIZATION='Token ' + response.data['token']) 

    def setup_goal(self):
        set_up_url = "/goals/api/"
        set_up_data = {
            "name": "New goal",
            "description": "describe this",
            "completed": "false",
        }
        set_up_response = self.auth_client.post(set_up_url, set_up_data, format='json')
        self.assertEqual(set_up_response.status_code, status.HTTP_201_CREATED)
        return set_up_response.data['id']


    def test_get_goals_without_auth(self):
        url = "/goals/api/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_goal(self):
        url = "/goals/api/"
        self.auth_helper()
        data = {
            "name": "New goal",
            "description": "describe this",
            "completed": "false",
        }
        response = self.auth_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(Goal.objects.get().name, "New goal")
        self.assertEqual(Goal.objects.get().description, "describe this")
        self.assertEqual(Goal.objects.get().completed, False)
        self.assertEqual(Goal.objects.get().user.id, User.objects.get().id)

    def test_get_goals(self):
        self.auth_helper()
        url = "/goals/api/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Goal.objects.count())

    def test_get_3_goals(self):
        self.auth_helper()
        for i in range(3):
            self.setup_goal()

        url = "/goals/api/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_goal(self):
        self.auth_helper()
        new_goal_id = self.setup_goal()

        url = f"/goals/api/{new_goal_id}/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_goal_id, response.data['id'])
        self.assertEqual(Goal.objects.get().name, "New goal")
        self.assertEqual(Goal.objects.get().description, "describe this")
        self.assertEqual(Goal.objects.get().completed, False)

    def test_update_goal(self):
        self.auth_helper()
        new_goal_id = self.setup_goal()

        url = f"/goals/api/{new_goal_id}/"
        data = {
            "name": "Changed goal",
            "description": "updated description",
            "completed": "true",
        }
        response = self.auth_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(response.data['id'], Goal.objects.get().id)
        self.assertEqual(Goal.objects.get().name, "Changed goal")
        self.assertEqual(Goal.objects.get().description, "updated description")
        self.assertEqual(Goal.objects.get().completed, True)
        self.assertEqual(response.data['user'], Goal.objects.get().user.id)


    def test_delete_goal(self):
        self.auth_helper()
        new_goal_id = self.setup_goal()
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(new_goal_id, Goal.objects.get().id)

        url = f"/goals/api/{new_goal_id}/"
        data = {}
        response = self.auth_client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 0)

