import datetime
from os import access
from rest_framework import status
import pytest
from reserve.models import MenuReservation, Menu, Food, User
from model_bakery import baker



@pytest.mark.django_db
class TestReserve:
    def test_if_admin_reserved_returns_200(self, api_client):

        menu = baker.make(Menu, make_m2m=True)

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        foods = menu.foods.all()
                
        data = {'food_id': foods[0].id, "menu_id": menu.id, "quantity": 3}


        response2 = api_client.post(f'/reserve/?user_id={user.id}', data, headers=headers)

        assert response2.status_code == status.HTTP_201_CREATED

    

    def test_if_normal_user_reserved_returns_200(self, api_client):

        menu = baker.make(Menu, make_m2m=True)

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        foods = menu.foods.all()
                
        data = {'food_id': foods[0].id, "menu_id": menu.id, "quantity": 3}


        response2 = api_client.post(f'/reserve/', data, headers=headers)

        assert response2.status_code == status.HTTP_201_CREATED



    def test_if_food_not_in_menu_returns_404(self, api_client):

        menu = baker.make(Menu, make_m2m=True)
        food = baker.make(Food)

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
                
        data = {'food_id': food.id, "menu_id": menu.id, "quantity": 3}


        response2 = api_client.post(f'/reserve/', data, headers=headers)

        assert response2.status_code == status.HTTP_404_NOT_FOUND

    
    def test_if_user_edits_reservation_returns_true(self, api_client):

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation, user=user, quantity=5)
                
        data = {"quantity": 3}

        response2 = api_client.patch(f'/reserve/?reserve_id={reservation.id}', data, headers=headers)

        assert response2.data['quantity'] == 3


    def test_if_user_deletes_reservation_returns_204(self, api_client):

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation, user=user)

        response2 = api_client.delete(f'/reserve/?reserve_id={reservation.id}', headers=headers)

        assert response2.status_code == status.HTTP_204_NO_CONTENT


    def test_if_user_deletes_other_reservations_returns_403(self, api_client):

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation)

        response2 = api_client.delete(f'/reserve/?reserve_id={reservation.id}', headers=headers)

        assert response2.status_code == status.HTTP_403_FORBIDDEN


    def test_if_user_edits_other_reservation_returns_403(self, api_client):

        user = User.objects.create_user(
        first_name='user',
        last_name='last',
        email='user@gmail.com',
        username='user',
        password='foodreserve1')

        api_client.force_authenticate(user=user)

        response1 = api_client.post('/login/', {'username': 'user', 'password': 'foodreserve1'})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation, quantity=5)
                
        data = {"quantity": 3}

        response2 = api_client.patch(f'/reserve/?reserve_id={reservation.id}', data, headers=headers)

        assert response2.status_code == status.HTTP_403_FORBIDDEN


    def test_if_admin_edits_reservation_returns_true(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation, quantity=5)
                
        data = {"quantity": 3}

        response2 = api_client.patch(f'/reserve/?reserve_id={reservation.id}', data, headers=headers)

        assert response2.data['quantity'] == 3


    def test_if_admin_deletes_reservation_returns_204(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'
        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        reservation = baker.make(MenuReservation)

        response2 = api_client.delete(f'/reserve/?reserve_id={reservation.id}', headers=headers)

        assert response2.status_code == status.HTTP_204_NO_CONTENT

    