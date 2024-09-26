import requests
from eskiz.client.sync import ClientSync
import pandas as pd
from django.conf import settings
import os
from datetime import datetime
from config.settings import SMS_EMAIL,SMS_PASSWORD

def export_messages_to_excel():
    from .models import UserMessage  # Modelni import qilish
    # Ma'lumotlarni querysetdan olish
    messages = UserMessage.objects.all().values()
    # DataFrame yaratish
    df = pd.DataFrame(list(messages))
    
    # Vaqt zonasi bilan datetime maydonlarini topish va vaqt zonasizga aylantirish
    for column in df.select_dtypes(include=['datetimetz']).columns:
        df[column] = df[column].dt.tz_localize(None)  # Vaqt zonasini olib tashlash
    
    # Fayl nomini hozirgi vaqt bilan yaratish
    filename = f"user_messages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    # Excel faylga yozish
    df.to_excel(file_path, index=False)
    
    return file_path


def send_sms(phone_number, message):

    eskiz_client = ClientSync(
        email=SMS_EMAIL,
        password=SMS_PASSWORD,
    )

    try:
        response = eskiz_client.send_sms(
            phone_number=phone_number,
            message=message
        )
        return response
    except Exception as e:
        print(f"SMS yuborishda xatolik: {e}")
        return None
