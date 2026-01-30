from rest_framework import serializers
from .models import PassportVerification


class PassportVerificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportVerification
        fields = ["status", "provider_reference", "failure_reason"]


class PassportVerificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportVerification
        fields = "__all__"
