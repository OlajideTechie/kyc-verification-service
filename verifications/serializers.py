from rest_framework import serializers
from .models import PassportVerification


class PassportVerificationCreateSerializer(serializers.Serializer):
    passport_number = serializers.CharField(max_length=20)
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField()

    class Meta:
        model = PassportVerification
        fields = "__all__"


    def create(self, validated_data):
        return PassportVerification.objects.create(**validated_data)


class PassportVerificationDetailSerializer(serializers.Serializer):
    class Meta:
        model = PassportVerification
        fields = "__all__"

    def get(self, request, verification_id):
        try:
            verification = PassportVerification.objects.get(id=verification_id)
        except PassportVerification.DoesNotExist:
            return None

        serializer = PassportVerificationDetailSerializer(verification)
        return serializer.data
