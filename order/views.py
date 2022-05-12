from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import OrderSerializer, NoPrintersException, OrderAlreadyHasChecksException
from .tasks import create_pdf_for_checks


class OrderView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        checks_id = serializer.save()
        create_pdf_for_checks.delay(checks_id)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except NoPrintersException as e:
            response = Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except OrderAlreadyHasChecksException as e:
            response = Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return response
