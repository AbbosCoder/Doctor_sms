from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from smsAPI.models import UserMessage
from smsAPI.utils import send_sms

def check_and_send_scheduled_messages():
    # Get all pending messages with send_time <= now
    messages = UserMessage.objects.filter(sms_status='pending', send_time__lte=now())
    
    for message in messages:
        print(f"Attempting to send message to {message.phone_number}...")
        text = 'Bu Eskiz dan test'
        success = send_sms(phone_number=message.phone_number, message=text)
        
        if success:
            message.sms_status = 'success'
            print(f"Message sent to {message.phone_number}")
        else:
            message.sms_status = 'error'
            print(f"Failed to send message to {message.phone_number}")
        
        message.save()
 
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_scheduled_messages, 'interval', minutes=1)
    scheduler.start()
