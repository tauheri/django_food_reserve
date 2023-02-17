Django Food Reserve Applicatin
=============

This is a food reserve backend application that has been developed using Django and Django rest-framework.
It contains client and Admin parts with several APIs as below:

- User sign-up and login
- Get the menu for a date range
- Reserve food
- Edit and Remove reservation
- Create, Remove and Update foods
- Admin get menu
- Create, Remove and Update Menu
- Export reservations to excel



Setup
-------------

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/thistermeh/django_food_reserve.git
$ cd django_food_reserve
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 foodreservenv
$ source ~/foodreservenv/bin/activate
```

Then install the dependencies:

```sh
(foodreservenv)$ pip3 install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:

```sh
(foodreservenv)$ python manage.py runserver
```
Now endpoints will be available at `http://127.0.0.1:8000/`.
Each endpoint address can be found in `reserve/urls.py` file.


Test
-------------

```sh
(foodreservenv)$ cd reserve/tests
(foodreservenv)$ pytest
```
