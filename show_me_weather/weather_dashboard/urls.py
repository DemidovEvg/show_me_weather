from django.urls import path
from .views import *


api_weather = ApiWeatherViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update'
})

urlpatterns = [
    path('',
         WheatherCommonView.as_view(),
         name='weather_list'),

    path('create/weather',
         AddWheatherView.as_view(),
         name='weather_create'),

    path('update/weather/<int:pk>',
         EditWeatherView.as_view(),
         name='weather_update'),

    path('delete/weather/<int:pk>',
         DeleteWeatherView.as_view(),
         name='weather_delete'),

    path('create/city',
         AddCityView.as_view(),
         name='city_create'),

    path('update/city/<int:pk>',
         EditCityView.as_view(),
         name='city_update'),

    path('delete/city/<int:pk>',
         DeleteCityView.as_view(),
         name='city_delete'),

    path('api/city/',
         ApiCityWeatherView.as_view(),
         name='api_city_weather'),

    path('api/weather',
         api_weather,
         name='api_weather'),
]
