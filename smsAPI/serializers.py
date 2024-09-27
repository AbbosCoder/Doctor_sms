from rest_framework import serializers
from .models import UserMessage, SentSMS
from rest_framework import serializers
from .models import SentSMS


class SentSMSSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = SentSMS
        fields = ['full_name', 'sending_time', 'sms_status']  # Include the desired fields

    def get_full_name(self, obj):
        return obj.user_message.full_name


class UserMessageSerializer(serializers.ModelSerializer):
    sent_sms = SentSMSSerializer(many=True, read_only=True)  # Nested serializer for SMS history

    class Meta:
        model = UserMessage
        fields = ['id', 'full_name', 'phone_number', 'address', 'birth_day', 'sending_time', 
                  'description', 'sms_status', 'user_status', 'created_at']  # Include SMS history
