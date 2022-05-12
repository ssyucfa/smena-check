import json

from rest_framework import serializers

from checks.models import Printer, Check, CheckStatus


class NoPrintersException(Exception):
    def __init__(self):
        self.message = 'No one printer in this point. You need to create printer.'


class OrderAlreadyHasChecksException(Exception):
    def __init__(self):
        self.message = 'Order already has checks. No need to create.'


class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    address = serializers.CharField()
    point_id = serializers.IntegerField()
    items = ItemSerializer(many=True)
    client = ClientSerializer()

    def save(self, **kwargs):
        order = json.dumps(self.data)

        printers = Printer.objects.filter(point_id=self.validated_data.get("point_id"))
        if not printers:
            raise NoPrintersException

        checks = Check.objects.filter(order_id=self.validated_data.get("id"))
        if checks:
            raise OrderAlreadyHasChecksException

        checks = Check.objects.bulk_create([
            Check(
                printer_id=printer.id,
                type=printer.check_type,
                order=order,
                status=CheckStatus.NEW,
                order_id=self.validated_data.get("id")
            )
            for printer in printers
        ])
        return [check.id for check in checks]