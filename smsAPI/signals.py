# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserMessage, SentSMS

@receiver(post_save, sender=UserMessage)
def create_sent_sms(sender, instance, created, **kwargs):
    # Only create a new SentSMS if the UserMessage's status changed to 'success'
    if not created and instance.sms_status == 'success':
        SentSMS.objects.create(
            user_message=instance,
            sending_time=instance.sending_time,  # Copy the sending time from UserMessage
            sms_status=instance.sms_status  # Copy the status (it should be 'success')
        )
