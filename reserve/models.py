from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    telegram_id = models.CharField(max_length=255, null=True, blank=True)


class Food(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='food/images', null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Menu(models.Model):
    date = models.DateField()
    foods = models.ManyToManyField(Food)
    isActive = models.BooleanField()

    def get_foods(self):
        return Food.objects.filter(menu=self)

    def __str__(self) -> str:
        return str(self.date) 


class MenuReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, null=True, related_name='reservations')
    food = models.ForeignKey(Food, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveSmallIntegerField()
    placed_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user) 