from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker


class SignUpTests(APITestCase):
    def decode_message(self, response):
        return eval(response._container[0].decode('utf-8'))['Message']

    def test_get_sign_up(self):
        url = "/signup/"
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.decode_message(response), "This is get method of Sign Up API")

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
