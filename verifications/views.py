from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema

from .models import PassportVerification
from .serializers import (
    PassportVerificationCreateSerializer,
    PassportVerificationDetailSerializer,
)
from .services.interswitch import verify_passport

@extend_schema(
    tags=["KYC Passport Verification"],
    request=PassportVerificationCreateSerializer,
    responses=PassportVerificationDetailSerializer)
class PassportVerificationCreateView(GenericAPIView):

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification = serializer.save(status="processing")

        result = verify_passport(verification.passport_number)

        if result["status"] == "verified":
            verification.status = "verified"
            verification.provider_reference = result.get("reference")
        else:
            verification.status = "failed"
            verification.failure_reason = result.get("reason")

        verification.save()

        return Response(
            PassportVerificationDetailSerializer(verification).data,
            status=status.HTTP_201_CREATED
        )

@extend_schema(tags=["KYC Passport Verification"])
class PassportRetryVerificationCreateView(GenericAPIView):
    serializer_class = PassportVerificationDetailSerializer

    def post(self, request, pk):
        verification = PassportVerification.objects.get(pk=pk)

        if verification.status not in ["failed", "expired", "requires_action"]:
            return Response(
                {"detail": "Retry not allowed for current status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        verification.status = "processing"
        verification.failure_reason = ""
        verification.save()

        result = verify_passport(verification.passport_number)

        if result["status"] == "verified":
            verification.status = "verified"
            verification.provider_reference = result.get("reference")
        else:
            verification.status = "failed"
            verification.failure_reason = result.get("reason")

        verification.save()

        return Response(
            PassportVerificationDetailSerializer(verification).data,
            status=status.HTTP_200_OK
        )
    
@extend_schema(tags=["KYC Passport Verification"])
class PassportVerificationDetailView(GenericAPIView):
    serializer_class = PassportVerificationDetailSerializer
    queryset = PassportVerification.objects.all()

    def get(self, request, pk):
        verification = self.get_object_or_404(self.queryset, pk=pk)
        return Response(
            self.get_serializer(verification).data
        )
