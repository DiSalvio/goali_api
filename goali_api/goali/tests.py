from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from goali.models import Goal, Task, SubTask
from faker import Faker


class SignUpTests(APITestCase):
    def decode_message(self, response):
        return eval(response._container[0].decode('utf-8'))['Message']

    def test_get_sign_up(self):
        url = "/signup/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.decode_message(response), "This is get method of signup API")

    def test_valid_sign_up(self):

        before_users_count = len(User.objects.all())

        fake = Faker()
        url = "/signup/"
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "username": fake.first_name(),
            "password": "abcdefghijklmnop",
            "confirm_password": "abcdefghijklmnop"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.decode_message(response), "Successfully Signed up")
        self.assertEqual(len(User.objects.all()), before_users_count + 1)

    def test_missing_data_sign_up(self):

        before_users_count = len(User.objects.all())

        url = "/signup/"
        data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "username": "",
            "password": "",
            "confirm_password": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), before_users_count)

    def test_passwords_not_matching_sign_up(self):

        before_users_count = len(User.objects.all())

        fake = Faker()
        url = "/signup/"
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "username": fake.first_name(),
            "password": "abcdefghijklmnop",
            "confirm_password": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), before_users_count)


class GoalTests(APITestCase):
    def auth_helper(self):
        self.user = User.objects.create_user(username="stephen", password="12345678")
        url = "/login/"
        data = {
            "username": "stephen",
            "password": "12345678",
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

    def test_get_goals_without_auth(self):
        url = "/goals/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_goal(self):
        url = "/goals/"
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
        url = "/goals/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Goal.objects.count())

    def test_get_3_goals(self):
        self.auth_helper()
        for i in range(3):
            self.setup_goal()

        url = "/goals/"
        data = {}
        response = self.auth_client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_goal(self):
        self.auth_helper()
        new_goal_id = self.setup_goal()

        url = f"/goals/{new_goal_id}/"
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

        url = f"/goals/{new_goal_id}/"
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

        url = f"/goals/{new_goal_id}/"
        data = {}
        response = self.auth_client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 0)


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
