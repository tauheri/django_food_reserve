from rest_framework import status
from reserve.models import User
import pytest


@pytest.mark.django_db
class TestLogin:
    def test_if_wrong_password_returns_401(self, api_client):
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)

        response = api_client.post('/login/', {'username': 'user2', 'password': '1'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_wrong_username_returns_401(self, api_client): 
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)

        response = api_client.post('/login/', {'username': 'a', 'password': 'Django12345'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_wrong_password_and_username_returns_401(self, api_client): 
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)
       
        response = api_client.post('/login/', {'username': 'a', 'password': '1'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    
    def test_if_empty_password_or_username_returns_400(self, api_client):
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)
        
        response = api_client.post('/login/', {'username': '', 'password': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_correct_password_and_username_returns_200(self, api_client):
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)
        
        response = api_client.post('/login/', {'username': 'user2', 'password': 'Django12345'})

        assert response.status_code == status.HTTP_200_OK

    