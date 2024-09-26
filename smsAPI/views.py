from rest_framework import generics
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import UserMessage
from .serializers import UserMessageSerializer

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
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(sms_status='success')
