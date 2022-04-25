
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id',
                  'name',
                  'weather_set'
                  ]
        depth = 2

    def create(self, validated_data):
        print(111111111111111111)
        return None


class PsevdoCitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True, max_length=255)


class WeatherSerializer(serializers.ModelSerializer):
    city = PsevdoCitySerializer()

    class Meta:
        model = WeatherInCities
        fields = ['id',
                  'date',
                  'hour',
                  'city',
                  'temperature',
                  'weather',
                  ]
        depth = 1

    def create(self, validated_data):
        city_data = validated_data.pop('city')
        city = get_object_or_404(City, id=city_data.get(
            'id'), name=city_data.get('name'))
        weather = WeatherInCities.objects.create(city=city, **validated_data)
        return weather
