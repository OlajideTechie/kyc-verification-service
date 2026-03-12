import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .models import PassportVerification
from .serializers import (
    PassportVerificationCreateSerializer,
    PassportVerificationDetailSerializer,
)
from services.interswitch import InterswitchClient


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["KYC Passport Verification"],
    request=PassportVerificationCreateSerializer,
)
class PassportVerificationCreateView(GenericAPIView):

    serializer_class = PassportVerificationCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logger.info("Starting passport verification")

        verification = serializer.save(status="processing")

        try:
            client = InterswitchClient()

            token = client.authenticate()

            payload = {
                "passport_number": verification.passport_number,
                "last_name": verification.last_name,
                "date_of_birth": verification.date_of_birth.isoformat(),
            }

            result = client.verify_passport(token=token, payload=payload)

            logger.info("Received response from Interswitch")

            verification.provider_response = result

            if result.get("code") == "200":
                verification.status = "verified"
                verification.provider_reference = result.get("reference_id")

            else:
                verification.status = "failed"
                verification.failure_reason = result.get("message")

            verification.save()

            return Response(
                {
                    "status": True,
                    "verification_id": verification.id,
                    "result": result,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as exc:

            logger.exception("Passport verification failed")

            verification.status = "failed"
            verification.failure_reason = str(exc)
            verification.save(update_fields=["status", "failure_reason"])

            return Response(
                {
                    "status": False,
                    "message": "KYC verification failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["KYC Passport Verification"],
)
class PassportVerificationDetailView(GenericAPIView):

    serializer_class = PassportVerificationDetailSerializer
    permission_classes = [AllowAny]

    def get(self, request, verification_id):

        verification = get_object_or_404(
            PassportVerification,
            id=verification_id,
        )

        if verification.status == "verified":
            message = "KYC verification successful"
            status_flag = True

        elif verification.status == "failed":
            message = verification.failure_reason or "KYC verification failed"
            status_flag = False

        else:
            message = "Verification in progress"
            status_flag = False

        return Response(
            {
                "status": status_flag,
                "result": verification.provider_response,
                "message": message,
            },
            status=status.HTTP_200_OK,
        )