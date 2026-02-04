from http.client import responses
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny as allow_any
from urllib3 import request
from .models import PassportVerification
from .serializers import (
    PassportVerificationCreateSerializer,
    PassportVerificationDetailSerializer,
)
from .services.interswitch import InterswitchClient
from rest_framework.generics import CreateAPIView, RetrieveAPIView

logger = logging.getLogger(__name__)

@extend_schema(
    tags=["KYC Passport Verification"],
    request=PassportVerificationCreateSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "status": {"type": "boolean"},
                "message": {"type": "string"},
            },
        }
    },
)
class PassportVerificationCreateView(GenericAPIView):
    serializer_class = PassportVerificationCreateSerializer
    permission_classes = [allow_any]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logger.info("Starting passport verification process")

        verification = serializer.save(status="processing")

        try: 
           interswitch_client = InterswitchClient()
           token = interswitch_client.authenticate()

           result = interswitch_client.verify_passport(
               token=token,
                payload={
                    "passport_number": verification.passport_number,
                    "last_name": verification.last_name,
                    "date_of_birth": verification.date_of_birth.isoformat(),
                },
            )
           
           # Update verification record based on response
           verification.provider_response = result

           logger.info(f"Received response from Interswitch: {result}")
           
           if result.get("code") == "200":
                verification.status = "verified"
                verification.provider_reference = result.get("reference_id")
             
           else:
                verification.status = "failed"
                verification.failure_reason = result.get("message")
       
            # Save the updated verification record
           verification.save()
                 
           return Response({
                "verification_id": verification.id,
                "result": result,
           }, status=status.HTTP_200_OK)
                
           
        except Exception as e:
               logger.error(f"Error during passport verification: {str(e)}")
               verification.status = "failed"
               verification.failure_reason = str(e)
               verification.save()

               logger.info("Passport verification process ended with failure")

               return Response(
                    {"status": False, "message": "KYC Verification failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    
    
    

@extend_schema(
    tags=["KYC Passport Verification"],
    responses={200: {"type": "object", "properties": {"status": {"type": "boolean"}, "message": {"type": "string"}}}}
)
class PassportVerificationDetailView(GenericAPIView):
    permission_classes = [allow_any]

    def get(self, request, verification_id):
        verification = get_object_or_404(PassportVerification, id=verification_id)
        
        if verification.status == "verified":
            message = "KYC registration successful"
            status_flag = True
        elif verification.status == "failed":
            message = verification.failure_reason or "KYC Verification failed"
            status_flag = False
        else:
            message = "Verification in progress"
            status_flag = False

        return Response(
            {"status": status_flag, "message": message},
            status=status.HTTP_200_OK
        )