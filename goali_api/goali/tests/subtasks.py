from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from goali.models import Goal, Task, SubTask


class SubTaskTests(APITestCase):
    def auth_helper(self):
        self.user = User.objects.create_user(username="thomas", password="ladder")
        url = "/login/"
        data = {
            "username": "thomas",
            "password": "ladder",
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

    def setup_subtask(self, setup_goal_id, setup_task_id):
        set_up_url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/"
        set_up_data = {
            "name": "A sub task",
            "description": "A descriptive description",
            "completed": "true",
            "goal": setup_goal_id,
            "task": setup_task_id
        }
        set_up_response = self.auth_client.post(set_up_url, set_up_data, format='json')
        self.assertEqual(set_up_response.status_code, status.HTTP_201_CREATED)
        return set_up_response.data['id']

    def test_get_subtasks_without_auth(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_subtask(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/"
        data = {
            "name": "Sub-Task Name",
            "description": "it is below a task",
            "completed": "true",
        }
        response = self.auth_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 1)
        self.assertEqual(SubTask.objects.get().name, "Sub-Task Name")
        self.assertEqual(SubTask.objects.get().description, "it is below a task")
        self.assertEqual(SubTask.objects.get().completed, True)
        self.assertEqual(SubTask.objects.get().user.id, User.objects.get().id)
        self.assertEqual(SubTask.objects.get().goal.id, Goal.objects.get().id)
        self.assertEqual(SubTask.objects.get().task.id, Task.objects.get().id)

    def test_get_subtasks(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), SubTask.objects.count())

    def test_get_3_subtasks(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        for i in range(3):
            self.setup_subtask(setup_goal_id, setup_task_id)

        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_subtask(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        new_subtask_id = self.setup_subtask(setup_goal_id, setup_task_id)

        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/{new_subtask_id}/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_subtask_id, response.data['id'])
        self.assertEqual(SubTask.objects.get().name, "A sub task")
        self.assertEqual(SubTask.objects.get().description, "A descriptive description")
        self.assertEqual(SubTask.objects.get().completed, True)
        self.assertEqual(SubTask.objects.get().goal_id, setup_goal_id)
        self.assertEqual(SubTask.objects.get().task_id, setup_task_id)

    def test_update_subtask(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        new_subtask_id = self.setup_subtask(setup_goal_id, setup_task_id)

        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/{new_subtask_id}/"
        data = {
            "name": "Changed sub-task",
            "description": "updated sub-task description",
            "completed": "true",
            "removed": "false"
        }
        response = self.auth_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.count(), 1)
        self.assertEqual(response.data['id'], SubTask.objects.get().id)
        self.assertEqual(SubTask.objects.get().name, "Changed sub-task")
        self.assertEqual(SubTask.objects.get().description, "updated sub-task description")
        self.assertEqual(SubTask.objects.get().completed, True)
        self.assertEqual(SubTask.objects.get().goal_id, setup_goal_id)
        self.assertEqual(SubTask.objects.get().task_id, setup_task_id)
        self.assertEqual(response.data['user'], SubTask.objects.get().user.id)

    def test_delete_subtask(self):
        self.auth_helper()
        setup_goal_id = self.setup_goal()
        setup_task_id = self.setup_task(setup_goal_id)
        new_subtask_id = self.setup_subtask(setup_goal_id, setup_task_id)

        self.assertEqual(SubTask.objects.count(), 1)
        self.assertEqual(new_subtask_id, SubTask.objects.get().id)

        url = f"/goals/{setup_goal_id}/tasks/{setup_task_id}/subtasks/{new_subtask_id}/"
        data = {}
        response = self.auth_client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.count(), 0)
