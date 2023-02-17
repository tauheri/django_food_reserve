from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'username', 'telegram_id']


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price']


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'isActive']


@admin.register(models.MenuReservation)
class MenuReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu', 'food', 'quantity', 'placed_at']
