from django.db import models
from django.urls import reverse

{1: 1, 2: 2}


class Weather:
    weather = {
        'Снег': {
            'is_right_temperature': lambda temp: temp <= 0,
            'is_right_hour': lambda hour: True,
        },
        'Дождь': {
            'is_right_temperature': lambda temp: temp >= 0,
            'is_right_hour': lambda hour: True,
        },
        'Солнце': {
            'is_right_temperature': lambda temp: True,
            'is_right_hour': lambda hour: 8 <= hour <= 19,
        },
        'Облачность': {
            'is_right_temperature': lambda temp: True,
            'is_right_hour': lambda hour: True,
        },
    }

    @classmethod
    def get_weather_choices(cls):
        return [(w, w) for w in cls.weather.keys()]

    @classmethod
    def is_right_temperature(cls, weather, temperature):
        return cls.weather[weather]['is_right_temperature'](temperature)

    @classmethod
    def is_right_hour(cls, weather, hour):
        return cls.weather[weather]['is_right_hour'](hour)


class WeatherInCities(models.Model):
    HOURS_CHOICES = [(hour, hour) for hour in range(25)]
    date = models.DateField(verbose_name='Дата')
    hour = models.PositiveSmallIntegerField(
        verbose_name='Время(часы)',
        help_text='Выберете время (час)',
        choices=HOURS_CHOICES,
        default=0
    )
    city = models.ForeignKey(
        verbose_name='Город',
        to='City',
        on_delete=models.CASCADE,
        related_name='weather_set'
    )
    temperature = models.SmallIntegerField(verbose_name='Температура')
    weather = models.CharField(
        verbose_name='Погода',
        choices=Weather.get_weather_choices(),
        max_length=50,
        default='Солнце')

    def get_absolute_url(self):
        return reverse('weather_city', kwargs={'pk': self.pk})

    def __str__(self):
        return (f'{self.date = } '
                f'{self.hour = } '
                f'{self.city = } '
                f'{self.temperature = } '
                f'{self.weather = }')

    class Meta:
        verbose_name = 'Погода в городе'
        verbose_name_plural = 'Погода в городах'
        ordering = ('date', 'hour')
        unique_together = [['city', 'date', 'hour']]


class City(models.Model):
    name = models.CharField(verbose_name='Название города',
                            max_length=255,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('name', )
