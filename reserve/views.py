from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from .models import Food, MenuReservation, Menu, User
from .serializers import MenuReservationSerializer, UserSerializer, TelegramUserSerializer, FoodSerializer, MenuSerializer, NormalUsersMenuSerializer, MyTokenObtainPairSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
# from django.contrib.auth.models import User
from django.db.models import Prefetch
import datetime
import calendar
import pandas as pd
from io import BytesIO
from django.http import StreamingHttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
import jdatetime
from persiantools import digits



class LoginView(TokenObtainPairView):
	"""
	Login View with jWt token authentication
	"""
	serializer_class = MyTokenObtainPairSerializer


class MenuList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        
        if request.query_params:

            if request.query_params['date1'] <= request.query_params['date2']:

                begin = request.query_params['date1']

                end = request.query_params['date2']

            else:

                begin = request.query_params['date2']

                end = request.query_params['date1']

        else:

            today = datetime.date.today()

            weekday = calendar.day_name[today.weekday()]

            if weekday == 'Saturday':
                begin = today
                end = today + datetime.timedelta(5)

            elif weekday == 'Sunday':
                begin = today - datetime.timedelta(1)
                end = today + datetime.timedelta(4)

            elif weekday == 'Monday':
                begin = today - datetime.timedelta(2)
                end = today + datetime.timedelta(3)

            elif weekday == 'Tuesday':
                begin = today - datetime.timedelta(3)
                end = today + datetime.timedelta(2)

            elif weekday == 'Wednesday':
                begin = today - datetime.timedelta(4)
                end = today + datetime.timedelta(1)
            
            elif weekday == 'Thursday':
                begin = today - datetime.timedelta(5)
                end = today 

            elif weekday == 'Friday':
                begin = today - datetime.timedelta(6)
                end = today - datetime.timedelta(1)


        if request.user.is_superuser:

            queryset = get_list_or_404(Menu.objects.order_by('date'), date__range=(begin, end))

            serializer = MenuSerializer(queryset, many=True, context={"request": request})

            return Response(serializer.data)

        else:

            try:

                queryset = Menu.objects.prefetch_related(
                    Prefetch(
                        'reservations', 
                        queryset=MenuReservation.objects.filter(user__id=request.user.id),
                        to_attr='filtered_reservations')
                ).filter(date__range=(begin, end)).order_by('date')

                serializer = NormalUsersMenuSerializer(queryset, many=True, context={"request": request})

                return Response(serializer.data)

            except Menu.DoesNotExist:

                return Response(status = status.HTTP_404_NOT_FOUND)



class Reserve(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        reserve_id = request.query_params['reserve_id']

        reservation = get_object_or_404(MenuReservation, id = reserve_id)

        serializer = MenuReservationSerializer(reservation, context={"request": request})

        return Response(serializer.data)

    
    def post(self, request):

        if request.user.is_superuser:

            user_id = request.query_params['user_id']

        else:

            user_id = request.user.id

        try:
            #{"menu_id":1,"food_id":1,"quantity":4}

            food_id = int(request.data['food_id'])
            menu_id = int(request.data['menu_id'])
            quantity = int(request.data['quantity'])
          
            queryset = Menu.objects.filter(id = menu_id)

            foodIds = []

            for item in list(queryset.values('foods__id')):
                foodIds.append(item['foods__id'])

            if food_id in foodIds:

                menu = Menu.objects.get(id = menu_id)
                food = Food.objects.get(id = food_id)
                user = User.objects.get(id = user_id)

                new_reservation = MenuReservation(
                    user = user,
                    menu = menu,
                    food = food,
                    quantity = quantity
                )

                new_reservation.save()

                return Response(
                    {
                        'Success': True, 
                        'Massage': 'Food reserved successfully.'
                    },
                    status = status.HTTP_201_CREATED
                )

            else:

                return Response(
                    {
                        'Success': False, 
                        'Massage': 'This food is not in the menu!'
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

        except Menu.DoesNotExist:

            return Response(
                {
                    'Success': False, 
                    'Massage': 'The menu does not exist!'
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request):

        reserve_id = request.query_params['reserve_id']

        if not(request.user.is_superuser):

            user_id = request.user.id

            [userId] = list(MenuReservation.objects.filter(id = reserve_id).values('user__id'))

            if user_id != userId['user__id']:

                return Response("You do not have the permision to update this reservation",
                                status = status.HTTP_403_FORBIDDEN)

        reservation = get_object_or_404(MenuReservation, id = reserve_id)

        data = request.data

        try:

            reservation.user = User.objects.get(id=data['user_id'])

        except KeyError:

            pass
        # reservation.menu = Menu.objects.get(id=data['menu']['id'])
        
        try:

            reservation.food = Food.objects.get(id=data['food_id'])

        except KeyError:

            pass
        
        reservation.quantity = data.get('quantity', reservation.quantity)
        # reservation.placed_at = data.get('placed_at', reservation.placed_at)

        reservation.save()

        serializer = MenuReservationSerializer(reservation, context={"request": request})

        return Response(serializer.data)
    

    def delete(self, request):

        reserve_id = request.query_params['reserve_id']

        if not(request.user.is_superuser):     

            user_id = request.user.id

            [userId] = list(MenuReservation.objects.filter(id = reserve_id).values('user__id'))

            if user_id != userId['user__id']:

                return Response("You do not have the permision to delete this reservation",
                                status = status.HTTP_403_FORBIDDEN)


        reservation = get_object_or_404(MenuReservation, id = reserve_id)

        reservation.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class Foods(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        if request.query_params:

            food_id = request.query_params['food_id']

            food = get_object_or_404(Food, id = food_id)

            serializer = FoodSerializer(food, context={"request": request})

            return Response(serializer.data)
        
        queryset = Food.objects.all()

        serializer = FoodSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data)

    
    def post(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        #{"title":"","description":"","price":40000,"discount":5, "image":""}

        title = request.data['title']
        description = request.data['description']
        price = float(request.data['price'])
        discount = request.data.get('discount', None)
        image = request.data.get('image', None)

        if discount is not None:
            discount = float(discount)

        new_food = Food(
            title = title,
            description = description,
            price = price,
            discount = discount,
            image = image
        )

        new_food.save()

        return Response(
            {
                'Success': True, 
                'Massage': 'Food created successfully.'
            },
            status = status.HTTP_201_CREATED
        )

    
    def patch(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        food_id = request.query_params['food_id']

        food = get_object_or_404(Food, id = food_id)

        data = request.data
        
        food.title = data.get('title', food.title)
        food.description = data.get('description', food.description)
        food.price = data.get('price', food.price)
        food.discount = data.get('discount', food.discount)
        food.image = data.get('image', food.image)

        food.save()

        serializer = FoodSerializer(food, context={"request": request})

        return Response(serializer.data)
    

    def delete(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        food_id = request.query_params['food_id']

        food = get_object_or_404(Food, id = food_id)

        food.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class MenuAdmin(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        if request.query_params:

            menu_id = request.query_params['menu_id']

            menu = get_object_or_404(Menu, id = menu_id)

            serializer = MenuSerializer(menu, context={"request": request})

            return Response(serializer.data)

        queryset = Menu.objects.all()

        serializer = MenuSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data)

    
    def post(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        #{"date":"","foodIds":[food_ids],"isActive":True}

        foods = []

        for foodId in request.data['foodIds']:
            foods.append(get_object_or_404(Food, id = foodId))
        
        date = request.data['date']
        isActive = request.data['isActive']

        new_menu = Menu.objects.create(
            date = date,
            isActive = isActive,
        )

        new_menu.foods.set(foods)

        new_menu.save()

        return Response(
            {
                'Success': True, 
                'Massage': 'Menu created successfully.'
            },
            status = status.HTTP_201_CREATED
        )

    
    def patch(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        menu_id = request.query_params['menu_id']

        menu = get_object_or_404(Menu, id = menu_id)

        data = request.data
        
        menu.date = data.get('date', menu.date)

        try:

            foods = []

            for foodId in request.data['foodIds']:
                foods.append(get_object_or_404(Food, id = foodId))

            menu.foods.set(foods)

        except KeyError:

            pass

        menu.isActive = data.get('isActive', menu.isActive)

        menu.save()

        serializer = MenuSerializer(menu, context={"request": request})

        return Response(serializer.data)
    

    def delete(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        menu_id = request.query_params['menu_id']

        menu = get_object_or_404(Menu, id = menu_id)

        menu.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class ReservationReportExcel(APIView):

    persionWeek = {
        "0": "شنبه",
        "1": "یکشنبه",
        "2": "دوشنبه",
        "3": "سه شنبه",
        "4": "چهارشنبه",
        "5": "پنجشنبه",
        "6": "جمعه",
    }

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        if request.query_params:

            if request.query_params['date1'] <= request.query_params['date2']:

                begin = request.query_params['date1']

                end = request.query_params['date2']

            else:

                begin = request.query_params['date2']

                end = request.query_params['date1']

            queryset = get_list_or_404(Menu.objects.order_by('date'), date__range=(begin, end))

            menus = list(queryset)

            dates = []
            weekdays = []
            users = {}
            foods = {}

            allUsers = list(User.objects.all())
            allFoods = list(Food.objects.all())

            for food in allFoods:

                foods[f'{food.id}'] = {

                    "title": food.title,

                    "quantity": [0] * len(menus)
                }

            for user in allUsers:

                full_name = user.first_name + ' ' + user.last_name

                users[f'{user.username}'] = {

                    "id": user.id,

                    "full_name": full_name,

                    "reserves": [],

                    "totalQuantity": 0,

                    "totalPrice": 0
                }

            usernames = users.keys()

            for idx, menu in enumerate(menus): 

                date = menu.date

                jalili_date =  jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year) 

                weekday = jalili_date.weekday()
                day = jalili_date.day
                month = jalili_date.month
                year = jalili_date.year

                dates.append(digits.en_to_fa(str(year)) + '/' + digits.en_to_fa(str(month)) + '/' + digits.en_to_fa(str(day)))

                weekdays.append(self.persionWeek[f'{weekday}'])

                for username in usernames:

                    reserve = []

                    for reservation in menu.reservations.all():
                        
                        if reservation.user.id == users[username]['id']:

                            foods[f'{reservation.food.id}']['quantity'][idx] += reservation.quantity

                            users[username]['totalQuantity'] += reservation.quantity

                            if reservation.food.discount is not None:
                                price = reservation.food.price * (100.0 - float(reservation.food.discount)) * 0.01
                            
                            else:
                                price = reservation.food.price

                            users[username]['totalPrice'] += price * reservation.quantity

                            if reservation.quantity > 1:

                                reserve.append(reservation.food.title + '(' + str(reservation.quantity) + ')')

                            else:

                                reserve.append(reservation.food.title)

                    users[username]['reserves'].append('-'.join(reserve))

            #to make all arrays have same size
            dates.extend(['تعداد','هزینه'])
            weekdays.extend(['',''])
            
            data = {'تاریخ': dates,    
                    'روز': weekdays,
            }

            for foodd in foods:
                title = 'title'
                foods[foodd]['quantity'].extend(['',''])
                data[f'{foods[foodd][title]}'] = foods[foodd]['quantity']
            
            
            for uuser in users:
                fullNam = 'full_name'
                users[uuser]['reserves'].append(users[uuser]['totalQuantity'])
                users[uuser]['reserves'].append(users[uuser]['totalPrice'])
                data[f'{users[uuser][fullNam]}'] = users[uuser]['reserves']
            
            output = BytesIO()

            df1 = pd.DataFrame(data)
            df = df1.transpose()
            
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Report')
            worksheet = writer.sheets['Report']
            worksheet.right_to_left()
            writer.save()

            output.seek(0)

            output_name = 'monthly_report'
            response = StreamingHttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={output_name}.xlsx'
            return response
        
        return Response(status = status.HTTP_404_NOT_FOUND)



class TelegramUserAuthorization(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        if request.query_params:

            telegram_id = request.query_params['telegram_id']

            try:
                user = User.objects.get(telegram_id = telegram_id)

                serializer = TelegramUserSerializer(user)

                return Response(serializer.data)

            except User.DoesNotExist:

                return Response(
                    {
                        'UserExistence': False
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
        return Response(status = status.HTTP_404_NOT_FOUND)


    def patch(self, request):

        user = request.user

        data = request.data
        
        user.telegram_id = data.get('telegram_id', user.telegram_id)
        user.first_name = user.first_name
        user.last_name = user.last_name
        user.email = user.email
        user.username = user.username
        user.password = user.password

        user.save()

        return Response("telegram id updated!")



class TelegramUserCredintial(APIView):
    
    def get(self, request):

        if request.query_params:

            telegram_id = request.query_params['telegram_id']

            try:
                user = User.objects.get(telegram_id = telegram_id)

                return Response(
                    {
                        "UserExistence": True
                    },
                    status = status.HTTP_200_OK
                )

            except User.DoesNotExist:

                return Response(
                    {
                        'UserExistence': False
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
        return Response(status = status.HTTP_404_NOT_FOUND)



class UserAdmin(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        if not(request.user.is_superuser):

            return Response("Only admins have the permision to access this endpoint!",
                            status = status.HTTP_403_FORBIDDEN)

        if request.query_params:

            user_id = request.query_params['user_id']

            user = get_object_or_404(User, id = user_id)

            serializer = UserSerializer(user)

            return Response(serializer.data)

        queryset = User.objects.all()

        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)



class BotReserve(APIView):
    
    def get(self, request):

        user_id = request.query_params['user_id']

        today = datetime.date.today()

        try:

            queryset = Menu.objects.prefetch_related(
                Prefetch(
                    'reservations', 
                    queryset=MenuReservation.objects.filter(user__id=user_id),
                    to_attr='filtered_reservations')
            ).filter(date=today)

            serializer = NormalUsersMenuSerializer(queryset, many=True, context={"request": request})

            return Response(serializer.data)

        except Menu.DoesNotExist:

            return Response(status = status.HTTP_404_NOT_FOUND)

    
    def post(self, request):

        try:
            #{"user_id":1, "menu_id":1,"food_id":1,"quantity":4}

            user_id = request.data['user_id']
            food_id = int(request.data['food_id'])
            menu_id = int(request.data['menu_id'])
            quantity = int(request.data['quantity'])
          
            queryset = Menu.objects.filter(id = menu_id)

            foodIds = []

            for item in list(queryset.values('foods__id')):
                foodIds.append(item['foods__id'])

            if food_id in foodIds:

                menu = Menu.objects.get(id = menu_id)
                food = Food.objects.get(id = food_id)
                user = User.objects.get(id = user_id)

                new_reservation = MenuReservation(
                    user = user,
                    menu = menu,
                    food = food,
                    quantity = quantity
                )

                new_reservation.save()

                return Response(
                    {
                        'Success': True, 
                        'Massage': 'Food reserved successfully.'
                    },
                    status = status.HTTP_201_CREATED
                )

            else:

                return Response(
                    {
                        'Success': False, 
                        'Massage': 'This food is not in the menu!'
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

        except Menu.DoesNotExist:

            return Response(
                {
                    'Success': False, 
                    'Massage': 'The menu does not exist!'
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request):

        reserve_id = request.query_params['reserve_id']

        reservation = get_object_or_404(MenuReservation, id = reserve_id)

        data = request.data

        try:

            reservation.user = User.objects.get(id=data['user_id'])

        except KeyError:

            pass
        
        try:

            reservation.food = Food.objects.get(id=data['food_id'])

        except KeyError:

            pass
        
        reservation.quantity = data.get('quantity', reservation.quantity)

        reservation.save()

        serializer = MenuReservationSerializer(reservation, context={"request": request})

        return Response(serializer.data)
    

    def delete(self, request):

        reserve_id = request.query_params['reserve_id']

        reservation = get_object_or_404(MenuReservation, id = reserve_id)

        reservation.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class BotGetUser(APIView):
    
    def get(self, request):

        if request.query_params:

            telegram_id = request.query_params['telegram_id']

            try:
                user = User.objects.get(telegram_id = telegram_id)

                serializer = TelegramUserSerializer(user)

                return Response(serializer.data)

            except User.DoesNotExist:

                return Response(
                    {
                        'UserExistence': False
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
        return Response(status = status.HTTP_404_NOT_FOUND)