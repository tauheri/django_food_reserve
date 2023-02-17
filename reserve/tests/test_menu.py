import datetime
from os import access
from rest_framework import status
import pytest
from reserve.models import Menu, User
from model_bakery import baker



@pytest.mark.django_db
class TestRetrieveMenu:
    def test_if_menu_exists_with_no_dates_and_admin_login_returns_200(self, api_client):
        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)
        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
        
        today = datetime.date.today()
        menu1 = baker.make(Menu, date=today, make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 12), make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 15), make_m2m=True)

        response2 = api_client.get('/menu/', headers=headers)

        assert response2.status_code == status.HTTP_200_OK
        # assert len(response2.data) == 2

    
    def test_if_menu_exists_with_dates_and_admin_login_returns_returns_200(self, api_client):
        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)
        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
        
        menu1 = baker.make(Menu, date=datetime.date(2022, 8, 2), make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 4), make_m2m=True)

        begin = datetime.date(2022, 8, 2)
        end = datetime.date(2022, 8, 2)

        data = {'date1': begin, "date2": end}

        response2 = api_client.get('/menu/', data, headers=headers)

        assert response2.status_code == status.HTTP_200_OK
        assert len(response2.data) == 1

    
    def test_if_menu_exists_with_normal_user_login_returns_200(self, api_client):
        
        user = User.objects.create_user(
        first_name='user2',
        last_name='last2',
        email='user2@gmail.com',
        username='user2',
        password='Django12345')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user2', 'password': 'Django12345'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
        
        menu1 = baker.make(Menu, date=datetime.date(2022, 8, 2), make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 4), make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 15), make_m2m=True)

        response2 = api_client.get('/menu/', headers=headers)

        assert response2.status_code == status.HTTP_200_OK
        # assert len(response2.data) == 2

    
    def test_if_menu_not_exists_with_dates_returns_404(self, api_client):
        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)
        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
        
        menu1 = baker.make(Menu, date=datetime.date(2022, 8, 2), make_m2m=True)
        menu2 = baker.make(Menu, date=datetime.date(2022, 8, 4), make_m2m=True)

        begin = datetime.date(2022, 8, 5)
        end = datetime.date(2022, 8, 10)

        data = {'date1': begin, "date2": end}

        response2 = api_client.get('/menu/', data, headers=headers)

        assert response2.status_code == status.HTTP_404_NOT_FOUND

