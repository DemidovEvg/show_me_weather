import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import (FormParser,
                                    MultiPartParser)
from rest_framework.response import Response
from rest_framework import status

from .forms import *
from .models import *
from .search_engine import *
from .serializer import *
from django.db.models import Count
from django.db.models import Prefetch


class WheatherCommonView(TemplateResponseMixin, View, SearchEngineMixin):
    template_name = 'weather_dashboard/weather_in_cities.html'

    def get_weather_with_filter(self,
                                date=None,
                                hour=None,
                                city=None,
                                temperature=None,
                                weather=None):

        weather_list = WeatherInCities.objects.all()

        result_query = Q()

        if date:
            result_query = result_query & self.get_query(fields_name='date',
                                                         parameter_value=date,
                                                         )

        if hour:
            result_query = result_query & self.get_query(fields_name='hour',
                                                         parameter_value=hour)

        if city:
            result_query = result_query & self.get_query(fields_name='city_id',
                                                         parameter_value=city)

        if isinstance(temperature, int):
            result_query = result_query & self.get_query(fields_name='temperature',
                                                         parameter_value=temperature)

        if weather:
            result_query = result_query & self.get_query(fields_name='weather',
                                                         parameter_value=weather)

        # breakpoint()
        weather_list = weather_list.filter(result_query)

        return weather_list

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Погода в городах'
        context['cities'] = (City.objects
                             .annotate(
                                 weather_set_count=Count('weather_set'))
                             .filter(weather_set_count__gt=0))

        if len(self.request.GET):
            context['form_weather_filter'] = WeatherFilterForm(
                self.request.GET)
            context['form_weather_filter'].is_valid()
            weather_list = self.get_weather_with_filter(
                context['form_weather_filter'].cleaned_data['date'],
                context['form_weather_filter'].cleaned_data['hour'],
                context['form_weather_filter'].cleaned_data['city'],
                context['form_weather_filter'].cleaned_data['temperature'],
                context['form_weather_filter'].cleaned_data['weather'],
            )
        else:
            weather_list = WeatherInCities.objects.all()
            context['form_weather_filter'] = WeatherFilterForm()

        context['form_weather'] = WeatherDashboardForm()

        context['form_city'] = CityForm()

        paginator = Paginator(weather_list, 20)

        cur_page_number = self.request.GET.get('page')

        page_obj = paginator.get_page(cur_page_number)

        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)


class AddWheatherView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form_weather'] = WeatherDashboardForm(request.POST)
        if context['form_weather'].is_valid():
            context['form_weather'].save()
            return redirect('weather_list')

        return self.render_to_response(context)


class AddCityView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form_city'] = CityForm(request.POST)
        if context['form_city'].is_valid():
            context['form_city'].save()
            return redirect('weather_list')

        return self.render_to_response(context)


class EditCityView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form_city'] = CityForm(request.POST)
        city = get_object_or_404(City, pk=self.kwargs['pk'])
        if context['form_city'].is_valid():
            city.name = context['form_city'].cleaned_data['name']
            city.save()
            return redirect('weather_list')

        context['city_edit_url'] = reverse(
            'city_update',
            args=[self.kwargs['pk']])

        context['city_edit_value'] = city.name

        return self.render_to_response(context)


class DeleteCityView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        city = get_object_or_404(City, pk=self.kwargs['pk'])
        city.delete()
        return redirect('weather_list')


class EditWeatherView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        weather = get_object_or_404(WeatherInCities, pk=self.kwargs['pk'])
        context['form_weather'] = WeatherDashboardForm(
            request.POST,
            instance=weather)
        if context['form_weather'].is_valid():
            weather.save()
            return redirect('weather_list')

        context['weather_edit_url'] = reverse(
            'weather_update',
            args=[self.kwargs['pk']])

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        weather = get_object_or_404(WeatherInCities, pk=self.kwargs['pk'])
        serializer = WeatherSerializer(weather)
        return JsonResponse(serializer.data)


class DeleteWeatherView(WheatherCommonView):
    def post(self, request, *args, **kwargs):
        weather = get_object_or_404(WeatherInCities, pk=self.kwargs['pk'])
        weather.delete()
        return redirect('weather_list')

    def get(self, request, *args, **kwargs):
        weather = get_object_or_404(WeatherInCities, pk=self.kwargs['pk'])
        serializer = WeatherSerializer(weather)
        return JsonResponse(serializer.data)


# ============== Rest =======================


class ApiCityWeatherView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        city_names = [v for k, v in self.request.GET.items() if 'city' in k]

        query_date = Q()
        if date_from:
            query_date = query_date & Q(date__gt=date_from)

        if date_to:
            query_date = query_date & Q(date__lt=date_to)

        weather = WeatherInCities.objects.filter(query_date)

        cities = City.objects.filter(name__in=city_names).prefetch_related(
            Prefetch('weather_set', queryset=weather))

        return cities


class ApiWeatherViewSet(viewsets.ModelViewSet):
    '''
    ModelViewSet автоматически добавляет методы list, create, retrive, update, destroy
    '''
    queryset = WeatherInCities.objects.all()

    serializer_class = WeatherSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        'date',
        'hour',
        'city',
        'temperature',
        'weather',
    )
    ordering_fields = ('date',)
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        json_file = request.data['json-file']
        data_string = json_file.read().decode('utf8')
        data_list = json.loads(data_string)

        result_data = []
        for data in data_list:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            result_data.append(serializer.data)

        headers = self.get_success_headers(serializer.data)

        return Response(result_data, status=status.HTTP_201_CREATED, headers=headers)
