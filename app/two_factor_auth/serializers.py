from rest_framework import serializers

from core.util import Validators


class SendVerificationTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17, validators=[Validators.phone_validator])

class CheckVerificationTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17, validators=[Validators.phone_validator])
    code = serializers.CharField(max_length=6)