from django.contrib import admin
from .models import *


@admin.register(WeatherInCities)
class WeatherInCitiesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'hour',
        'city',
        'temperature',
        'weather',
    )
    list_display_links = ('id', 'city')
    save_on_top = True
    list_filter = ('id',
        'date',
        'hour',
        'city',
        'temperature',
        'weather',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_display_links = ('id', 'name')
    save_on_top = True
