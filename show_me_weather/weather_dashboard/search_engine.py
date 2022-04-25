import urllib
from .models import *
from django.db.models import (Q,
                              QuerySet)


class SearchEngineMixin:
    def get_parameters_string(self, include_params: list[str] = None, exclude_params: list[str] = None):
        if include_params and include_params:
            raise Exception('Указаны и включаемые и исключаемые параметры')

        parameters = dict()
        if include_params:
            for parameter, value in self.request.GET.items():
                if parameter in include_params:
                    parameters[parameter] = value
        elif exclude_params:
            for parameter, value in self.request.GET.items():
                if parameter not in exclude_params:
                    parameters[parameter] = value

        return urllib.parse.urlencode(parameters)

    def get_query(self,
                  fields_name: list[str],
                  parameter_value: str,
                  ):

        if not isinstance(fields_name, list):
            fields_name = [fields_name]

        result_query = Q()

        for field_name in fields_name:
            query = Q(
                **{field_name: parameter_value})
            result_query = result_query.__and__(query)

        return result_query
