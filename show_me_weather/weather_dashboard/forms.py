from django import forms
from .models import *


class WeatherDashboardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = "Город не выбран"

    def clean(self):
        cleaned_data = super().clean()
        temperature = cleaned_data.get("temperature")
        hour = cleaned_data.get("hour")
        weather = cleaned_data.get("weather")
        errors = []
        if not Weather.is_right_temperature(weather, temperature):
            errors.append(forms.ValidationError(
                "Погода не совпадает с температурой",
                code='invalid'
            ))
        if not Weather.is_right_hour(weather, hour):
            errors.append(forms.ValidationError(
                "Погода не совпадает со временем",
                code='invalid'
            ))

        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        model = WeatherInCities
        fields = [
            'date',
            'hour',
            'city',
            'temperature',
            'weather'
        ]
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control',
                       }),
            'hour': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'weather': forms.Select(attrs={'class': 'form-control'}),
        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class WeatherFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(auto_id="id_%s_filter", *args, **kwargs)
        self.fields['date'].required = False
        self.fields['city'].required = False
        self.fields['temperature'].required = False
        self.fields['weather'].required = False

        self.fields['city'].empty_label = ""

    hour = forms.ChoiceField(label='Время(часы)',
                             required=False,
                             choices=[('', '')] +
                             WeatherInCities.HOURS_CHOICES,
                             widget=forms.Select(
                                   attrs={
                                       'class': 'form-control',
                                   }
                             ))

    weather = forms.ChoiceField(label='Погода',
                                required=False,
                                choices=[('', '')] +
                                Weather.get_weather_choices(),
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                    }
                                ))

    class Meta:
        model = WeatherInCities
        fields = [
            'date',
            'hour',
            'city',
            'temperature',
            'weather'
        ]
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control',
                       }),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
        }
