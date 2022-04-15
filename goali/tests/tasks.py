from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from goali.models import Task


class TaskTests(APITestCase):
    def auth_helper(self):
        self.user = User.objects.create_user(username="johnny", password="bagadonuts")
        url = "/login/"
        data = {
            "username": "johnny",
            "password": "bagadonuts",
        }
        response = self.client.post(url, data, format='json')
        self.auth_client = APIClient(HTTP_AUTHORIZATION='Token ' + response.data['token']) 

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

    def setup_task(self, setup_goal_id):
        set_up_url = f"/goals/{setup_goal_id}/tasks/"
        set_up_data = {
            "name": "New Task",
            "description": "describe task",
            "completed": "true",
            "goal": setup_goal_id
        }
        set_up_response = self.auth_client.post(set_up_url, set_up_data, format='json')
        self.assertEqual(set_up_response.status_code, status.HTTP_201_CREATED)
        return set_up_response.data['id']

    def test_get_tasks_without_auth(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        url = f"/goals/{setup_goal_id}/tasks/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        url = f"/goals/{setup_goal_id}/tasks/"
        data = {
            "name": "Task Name",
            "description": "describe task",
            "completed": "false",
        }
        response = self.auth_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, "Task Name")
        self.assertEqual(Task.objects.get().description, "describe task")
        self.assertEqual(Task.objects.get().completed, False)
        self.assertEqual(Task.objects.get().user.id, User.objects.get().id)

    def test_get_tasks(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        url = f"/goals/{setup_goal_id}/tasks/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.count())

    def test_get_3_tasks(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        for i in range(3):
            self.setup_task(setup_goal_id)

        url = f"/goals/{setup_goal_id}/tasks/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_task(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        new_task_id = self.setup_task(setup_goal_id)

        url = f"/goals/{setup_goal_id}/tasks/{new_task_id}/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_task_id, response.data['id'])
        self.assertEqual(Task.objects.get().name, "New Task")
        self.assertEqual(Task.objects.get().description, "describe task")
        self.assertEqual(Task.objects.get().completed, True)
        self.assertEqual(Task.objects.get().goal_id, setup_goal_id)

    def test_update_task(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        new_task_id = self.setup_task(setup_goal_id)

        url = f"/goals/{setup_goal_id}/tasks/{new_task_id}/"
        data = {
            "name": "Changed task",
            "description": "updated task description",
            "completed": "false",
            "removed": "false"
        }
        response = self.auth_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data['id'], Task.objects.get().id)
        self.assertEqual(Task.objects.get().name, "Changed task")
        self.assertEqual(Task.objects.get().description, "updated task description")
        self.assertEqual(Task.objects.get().completed, False)
        self.assertEqual(Task.objects.get().goal_id, setup_goal_id)
        self.assertEqual(response.data['user'], Task.objects.get().user.id)

    def test_delete_task(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        new_task_id = self.setup_task(setup_goal_id)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(new_task_id, Task.objects.get().id)

        url = f"/goals/{setup_goal_id}/tasks/{new_task_id}/"
        data = {}
        response = self.auth_client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 0)
