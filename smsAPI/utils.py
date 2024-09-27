from eskiz.client.sync import ClientSync
import environ

env = environ.Env()
environ.Env.read_env() 

SMS_EMAIL = str(env('SMS_EMAIL'))
SMS_PASSWORD = str(env('SMS_PASSWORD'))


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
