from rest_framework import generics, status
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import UserMessage, SentSMS
from .serializers import UserMessageSerializer, SentSMSSerializer
from rest_framework.response import Response

class SendSMSView(generics.UpdateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

    def perform_update(self, serializer):
        user_message = serializer.save()

        # Manually create a SentSMS record if the status is 'success'
        if user_message.sms_status == 'success':
            SentSMS.objects.create(
                user_message=user_message,
                sending_time=user_message.sending_time,  # Use the sending time from UserMessage
                sms_status=user_message.sms_status  # Set the status to 'success'
            )

class UserDetailView(generics.RetrieveAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    lookup_field = 'id'  # Assuming we're fetching by UUID

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Get related SentSMS records
        sent_sms_records = SentSMS.objects.filter(user_message=instance)
        sent_sms_serializer = SentSMSSerializer(sent_sms_records, many=True)
        return Response(serializer.data)

class UserMessageUpdateView(generics.UpdateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Check if sending_time is changed, then set sms_status to 'pending'
            if 'sending_time' in serializer.validated_data:
                instance.sms_status = 'pending'
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMessageCreateView(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

# Active Users API View
class ActiveUsersListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(user_status='active')

# Deactive Users API View
class DeactiveUsersListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(user_status='deactive')

# Today's SMS (Sent or to be sent today)
class TodaySMSListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return UserMessage.objects.filter(sending_time__date=today)

# Sent SMS (Success status today)
class SentTodaySMSListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return UserMessage.objects.filter(sms_status='success', sending_time__date=today)

# SMS sent this week
class SentThisWeekSMSListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        return UserMessage.objects.filter(sms_status='success', sending_time__date__gte=start_of_week)

# SMS sent this month
class SentThisMonthSMSListView(generics.ListAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return UserMessage.objects.filter(sms_status='success', sending_time__year=today.year, sending_time__month=today.month)

# All sent SMS
class AllSentSMSListView(generics.ListAPIView):
    serializer_class = SentSMSSerializer  # Use the SentSMSSerializer

    def get_queryset(self):
        return SentSMS.objects.all()  # Fetch all SentSMS records
