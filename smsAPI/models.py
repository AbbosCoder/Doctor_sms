import uuid
from django.db import models
from django.utils import timezone

SMS_STATUS = [
        ('pending', 'Kutilmoqda'),
        ('success', 'Yuborildi'),
        ('error', 'Rad etildi'),
    ]

USER_STATUS = [
        ('active', 'Davolanmoqda'),
        ('deactive', 'Davolanib bo\'lgan'),
    ]

class UserMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    birth_day = models.DateField()
    sending_time = models.DateTimeField()
    description = models.TextField()
    sms_status = models.CharField(max_length=10, choices=SMS_STATUS, default='pending')
    user_status = models.CharField(max_length=10, choices=USER_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

