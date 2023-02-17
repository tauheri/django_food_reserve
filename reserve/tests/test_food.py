from ntpath import join
import os
from pathlib import Path
from posixpath import dirname
from rest_framework import status
import pytest
from reserve.models import Food, User
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.mark.django_db
class TestFood:
    def test_if_admin_creates_food_returns_200(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'

        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}
                
        data = {"title":"قورمه سبزی",
                "description":"320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری",
                "price":82000,
                "discount":10}


        response2 = api_client.post(f'/food/', data, headers=headers)

        assert response2.status_code == status.HTTP_201_CREATED


    def test_if_admin_edits_food_returns_true(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'

        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        title = "قورمه سبزی"
        description = "320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری"
        price = 82000
        discount = 10     
                
        food = baker.make(Food, title=title, description=description, price=price, discount=discount)

        data = {"discount":5}

        response = api_client.patch(f'/food/?food_id={food.id}', data, headers=headers)

        assert response.data['discount'] == 5


    def test_if_admin_deletes_food_returns_204(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'

        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}   
                
        food = baker.make(Food)

        response = api_client.delete(f'/food/?food_id={food.id}', headers=headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_if_user_creates_food_returns_403(self, api_client):

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
                
        data = {"title":"قورمه سبزی",
                "description":"320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری",
                "price":82000,
                "discount":10}


        response2 = api_client.post(f'/food/', data, headers=headers)

        assert response2.status_code == status.HTTP_403_FORBIDDEN


    def test_if_admin_edits_food_image_returns_true(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'

        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}

        title = "قورمه سبزی"
        description = "320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری"
        price = 82000
        discount = 10     
                
        food = baker.make(Food, title=title, description=description, price=price, discount=discount)

        BASE_DIR = Path(__file__).resolve().parent.parent
        self.image =  os.path.join(BASE_DIR, "testImages/kebab.jpeg")

        (abs_dir_path, filename) = os.path.split(self.image)

        with open(self.image , 'rb') as f:
            _file = SimpleUploadedFile(filename, f.read())
    
            data = {"image":_file}

        response = api_client.patch(f'/food/?food_id={food.id}', data, headers=headers)

        assert response.data['image_url'] != None
    

    