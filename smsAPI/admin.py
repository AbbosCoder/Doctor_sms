from django.contrib import admin
from .models import UserMessage

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'sending_time', 'sms_status', 'user_status')
    
    # Making all fields readonly except sending_time
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields if field.name != 'sending_time']
        return []

    def save_model(self, request, obj, form, change):
        # When sending_time is changed, reset sms_status to 'pending'
        if 'sending_time' in form.changed_data:
            obj.sms_status = 'pending'
        super().save_model(request, obj, form, change)

admin.site.register(UserMessage, UserMessageAdmin)
