from django.db.models import QuerySet
from django.views import View
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request

from .models import CheckStatus


class NoProvideApiKeyException(Exception):
    def __init__(self):
        self.message = "You need to provide api_key"


class NoProvideCheckIdException(Exception):
    def __init__(self):
        self.message = "You need to provide check_id"


class QueryFilterMixin:
    @staticmethod
    def get_param_from_query(param_name: str, request: Request) -> str:
        param: str = request.query_params.get(param_name, "")
        return param.replace("\x00", "")


class CheckFilterBackend(QueryFilterMixin, BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view: View) -> QuerySet:
        api_key = self.get_param_from_query("api_key", request)
        check_id = self.get_param_from_query("check_id", request)
        if not api_key:
            raise NoProvideApiKeyException
        if not api_key and not check_id:
            raise NoProvideCheckIdException

        if api_key and check_id:
            return queryset.filter(printer__api_key=api_key, pk=check_id, status=CheckStatus.RENDERED)
        return queryset.filter(printer__api_key=api_key)

