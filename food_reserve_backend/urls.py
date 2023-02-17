from django.contrib import admin
from django.urls import include, path
# from food_reserve_bot import urls as food_reserve_bot_urls


admin.site.site_header = 'Food reserve Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('reserve.urls')),
    # path('food_reserve_bot/', include(food_reserve_bot_urls))
]