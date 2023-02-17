from rest_framework import status
import pytest
from reserve.models import Menu, Food, User
from model_bakery import baker
import datetime



@pytest.mark.django_db
class TestMenuAdmin:
    # def test_if_admin_creates_menu_returns_201(self, api_client):

    #     password = 'foodreserveadmin1'
    #     username = 'admin'

    #     admin = User.objects.create_superuser(username, 'admin@test.com', password)

    #     api_client.force_authenticate(user=admin)

    #     response1 = api_client.post('/login/', {'username': username, 'password': password})

    #     access_token = response1.data['access']

    #     headers = {'Authorization': f'JWT {access_token}'}

    #     title = "قورمه سبزی"
    #     description = "320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری"
    #     price = 82000
    #     discount = 10     
                
    #     food1 = baker.make(Food, title=title, description=description, price=price, discount=discount)
        
    #     today = datetime.date.today()

    #     data = {"date":today,
    #             "foodIds":[food1.id],
    #             "isActive":"True"}


    #     response2 = api_client.post(f'/menuadmin/', data, headers=headers)

    #     assert response2.status_code == status.HTTP_201_CREATED


    def test_if_admin_edits_menu_returns_true(self, api_client):

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
                
        food1 = baker.make(Food, title=title, description=description, price=price, discount=discount)
               
        date = "2022-08-15"
        isActive = True     
                
        menu = baker.make(Menu, date=date, foods=[food1], isActive=isActive)

        data = {"isActive":"False"}

        response = api_client.patch(f'/menuadmin/?menu_id={menu.id}', data, headers=headers)

        assert response.data['isActive'] == False


    def test_if_admin_deletes_menu_returns_204(self, api_client):

        password = 'foodreserveadmin1'
        username = 'admin'

        admin = User.objects.create_superuser(username, 'admin@test.com', password)

        api_client.force_authenticate(user=admin)

        response1 = api_client.post('/login/', {'username': username, 'password': password})

        access_token = response1.data['access']

        headers = {'Authorization': f'JWT {access_token}'}   
                
        menu = baker.make(Menu)

        response = api_client.delete(f'/menuadmin/?menu_id={menu.id}', headers=headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_if_user_creates_menu_returns_403(self, api_client):

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
                
        title = "قورمه سبزی"
        description = "320 گرم برنج صددرصد ایرانی، 300 گرم خورشت قورمه، 55 گرم گوشت گوساله، بسته بندی بهداشتی ماكروفری"
        price = 82000
        discount = 10     
                
        food1 = baker.make(Food, title=title, description=description, price=price, discount=discount)
                
        data = {"date":"2022-08-17",
                "foodIds":[food1.id],
                "isActive":"True"}


        response2 = api_client.post(f'/menuadmin/', data, headers=headers)

        assert response2.status_code == status.HTTP_403_FORBIDDEN
    

    