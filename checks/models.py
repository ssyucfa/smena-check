from django.db import models


class CheckType(models.TextChoices):
    KITCHEN = 'kt', 'Kitchen'
    CLIENT = 'cl', 'Client'


class CheckStatus(models.IntegerChoices):
    NEW = 1, 'new'
    RENDERED = 2, 'rendered'


class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    check_type = models.CharField(max_length=2, choices=CheckType.choices)
    point_id = models.IntegerField()


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=CheckType.choices)
    order = models.JSONField()
    order_id = models.IntegerField()
    status = models.IntegerField(choices=CheckStatus.choices)
    pdf = models.FileField(blank=True, null=True)
