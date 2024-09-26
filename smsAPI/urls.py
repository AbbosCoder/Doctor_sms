from django.urls import path
from .views import (
    ActiveUsersListView, DeactiveUsersListView,
    TodaySMSListView, SentTodaySMSListView,
    SentThisWeekSMSListView, SentThisMonthSMSListView,
    AllSentSMSListView
)

urlpatterns = [
    path('active-users/', ActiveUsersListView.as_view(), name='active-users'),
    path('deactive-users/', DeactiveUsersListView.as_view(), name='deactive-users'),
    path('sms/today/', TodaySMSListView.as_view(), name='today-sms'),
    path('sms/sent-today/', SentTodaySMSListView.as_view(), name='sent-today-sms'),
    path('sms/sent-this-week/', SentThisWeekSMSListView.as_view(), name='sent-this-week-sms'),
    path('sms/sent-this-month/', SentThisMonthSMSListView.as_view(), name='sent-this-month-sms'),
    path('sms/all-sent/', AllSentSMSListView.as_view(), name='all-sent-sms'),
]
