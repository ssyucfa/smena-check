from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import CheckFilterBackend, NoProvideApiKeyException, NoProvideCheckIdException
from .models import Check
from .serializers import CheckSerializer, CheckDetailSerializer


class CheckListView(GenericAPIView):
    queryset = Check.objects.all()
    filter_backends = [CheckFilterBackend]

    def get(self, request: Request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except NoProvideApiKeyException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except NoProvideCheckIdException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        if request.query_params.get('api_key') and request.query_params.get('check_id'):
            serializer = CheckDetailSerializer(queryset[0])
        else:
            serializer = CheckSerializer(queryset, many=True)
        return Response(serializer.data)
