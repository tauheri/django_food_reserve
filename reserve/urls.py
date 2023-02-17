from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('menu/', views.MenuList.as_view()),
    path('reserve/', views.Reserve.as_view()),
    path('food/', views.Foods.as_view()),
    path('menuadmin/', views.MenuAdmin.as_view()),
    path('login/', views.LoginView.as_view(), name='customlogin'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('report/', views.ReservationReportExcel.as_view()),
    path('telegramauth/', views.TelegramUserAuthorization.as_view()),
    path('telegramcred/', views.TelegramUserCredintial.as_view()),
    path('useradmin/', views.UserAdmin.as_view()),
    path('botreserve/', views.BotReserve.as_view()),
    path('botgetuser/', views.BotGetUser.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)