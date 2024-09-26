from django.apps import AppConfig

class SmsAPIConfig(AppConfig):
    name = 'smsAPI'

    def ready(self):
        from smsAPI.scheduler import start_scheduler
        start_scheduler()
