# REST_FRAMEWORK
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

# MODELS
from .models import AntiFraud

# SERIALIZERS
from.serializers import (SendVerificationTokenSerializer, 
                         CheckVerificationTokenSerializer)

# EXTERNAL LIBRARIES
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class TwoFactorAuthenticationViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'send_verification_token':
            return SendVerificationTokenSerializer
        elif self.action == 'check_verification_token':
            return CheckVerificationTokenSerializer
        return super().get_serializer_class()
    
    @action(methods=['post'],
        detail=False,
        url_name='send-verification-token',
        url_path='send-verification-token'
    )
    def send_verification_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        phone_number = serializer.validated_data['phone_number']

        try:
            verification = client.verify \
                                .v2 \
                                .services(os.environ['VERIFY_SERVICE_SID']) \
                                .verifications \
                                .create(to=phone_number, channel='sms')
            
            if verification.status:
                 antifraud = AntiFraud.objects.update_or_create(
                    phone_number=phone_number, 
                    defaults={
                        "last_status": "pending", 
                        "max_sequence_unapproved": 0
                    }
                )

            return Response({"status": verification.status}, status=status.HTTP_200_OK)
        except TwilioRestException as e:
            return Response(
                {"message": f"Sorry, an unexpected error ocurred. Error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    @action(methods=['post'],
        detail=False,
        url_name='check-verification-token',
        url_path='check-verification-token'
    )
    def check_verification_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        antifraud = AntiFraud.objects.get(phone_number=phone_number)
        max_attempts = 3
        
        if antifraud.max_sequence_unapproved >= max_attempts:
            return Response(
                {"message": "Sorry, you have exceeded the maximum number of attempts."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            verification_check = client.verify \
                                .v2 \
                                .services(os.environ['VERIFY_SERVICE_SID']) \
                                .verification_checks \
                                .create(
                                    to=phone_number, 
                                    code=code)
            
            if verification_check.status and verification_check.status == "pending":
                antifraud.last_status = verification_check.status
                antifraud.max_sequence_unapproved = antifraud.max_sequence_unapproved + 1
                antifraud.save()
                return Response({"status":verification_check.status}, status=status.HTTP_400_BAD_REQUEST)
            else:
                antifraud.last_status = verification_check.status
                antifraud.save()

            return Response({"status":verification_check.status}, status=status.HTTP_200_OK)
        except TwilioRestException as e:
            return Response(
                {"message": f"Sorry, an unexpected error ocurred. Error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

