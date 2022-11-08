import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')

application = get_wsgi_application()

from pprint import pprint

from rest_framework import status
# from django.urls import reverse
from rest_framework.test import APITestCase

# from django.contrib.auth.models import User
# from .models import CustomUser


# test the user registration endpoint
class RegistrationTestCase(APITestCase):

    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user = self.client.post(
            '/api/users/',
            data={"email": "bail@mail.com",
                  "username": "lynnch",
                  "first_name": "lol",
                  "last_name": "pupkin",
                  "password": "PASwwordLit"}
        )

    def test_registration(self):
        data = {"email": "mail@mail.com",
                "username": "lynn",
                "first_name": "lol",
                "last_name": "Пупкин",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pprint(response.data)

    def test_registration_unique_email(self):
        data = {"email": "bail@mail.com",
                "username": "lynda",
                "first_name": "lola",
                "last_name": "pupkin",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_unique_username(self):
        data = {"email": "tail@mail.ca",
                "username": "lynnch",
                "first_name": "lola",
                "last_name": "pupkin",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_without_email(self):
        data = {"email": "",
                "username": "lyna",
                "first_name": "Uasya",
                "last_name": "Vasiliy",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_without_username(self):
        data = {"email": "lil@mail.ru",
                "username": "",
                "first_name": "Uasya",
                "last_name": "Vasiliy",
                "password": ""}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_without_first_name(self):
        data = {"email": "lil@mail.com",
                "username": "lyna",
                "first_name": "",
                "last_name": "Пупкин",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_without_last_name(self):
        data = {"email": "ron@mail.ru",
                "username": "lyna",
                "first_name": "Uasya",
                "last_name": "",
                "password": "PASwwordLit"}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pprint(response.data)

    def test_registration_without_password(self):
        data = {"email": "rail@mail.ru",
                "username": "lyna",
                "first_name": "Uasya",
                "last_name": "Vasiliy",
                "password": ""}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data,
        # "{'password': [ErrorDetail(string='Это поле не может быть пустым.',
        # code='blank')]}")
        pprint(response.data)


# # test case for the userprofile model
# class UserProfileTestCase(APITestCase):
#     #profile_list_url = reverse('users')
#
#     def setUp(self):
#         # create a new user making a post request to djoser endpoint
#         self.user = self.client.post(
#             '/api/users/',
#             data={"email": "bail@mail.com",
#                   "username": "lynnch",
#                   "first_name": "lol",
#                   "last_name": "Пупкин",
#                   "password": "PASwwordLit"}
#         )
#         # obtain a json web token for the newly created user
#         response = self.client.post(
#             '/api/auth/token/login/',
#             data={'email': 'bail@mail.com', 'password': 'PASwwordLit'})
#         self.token = response.data['auth_token']
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
# #
# #     # retrieve a list of all user profiles while
# the request user is authenticated
#     def test_userprofile_list_authenticated(self):
#         response = self.client.get(self.user)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         pprint(response.data)
# #
# #     # retrieve a list of all user profiles while
# the request user is unauthenticated
# #     def test_userprofile_list_unauthenticated(self):
# #         self.client.force_authenticate(user=None)
# #         response = self.client.get(self.profile_list_url)
# #         self.assertEqual(response.status_code,
# status.HTTP_401_UNAUTHORIZED)
# #         pprint(response.data)
# #
# #     # check to retrieve the profile details of the authenticated user
# #     def test_userprofile_detail_retrieve(self):
# #         response = self.client.get(reverse('users', kwargs={'pk': 1}))
# #         # print(response.data)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #
# # # populate the user profile that was
#  automatically created using the signals
# #     def test_userprofile_profile(self):
# #         profile_data = {'description': 'I am a very famous game character',
# #                         'location': 'nintendo', 'is_creator': 'true', }
# #         response = self.client.put(reverse('profile', kwargs={'pk': 1}),
# #                                    data=profile_data)
# #         print(response.data)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
