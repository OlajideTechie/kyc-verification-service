from rest_framework import serializers
from .models import PassportVerification


class PassportVerificationCreateSerializer(serializers.Serializer):
    passport_number = serializers.CharField(max_length=20)


class PassportVerificationDetailSerializer(serializers.Serializer):
    class Meta:
        model = PassportVerification
        fields = "__all__"
