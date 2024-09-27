from eskiz.client.sync import ClientSync

SMS_EMAIL = 'xxxxxxxxx'
SMS_PASSWORD = 'xxxxxxxx'


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
    
send_sms(998947669933,'Bu Eskiz dan test')    
