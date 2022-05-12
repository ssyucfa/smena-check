from django.conf import settings
from rest_framework import serializers

from .models import Check


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = ("id", )


class CheckDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Check) -> dict[str, any]:
        representation = super().to_representation(instance)
        representation["pdf"] = settings.SITE_URL + instance.pdf.url
        return representation

    class Meta:
        model = Check
        fields = "__all__"
