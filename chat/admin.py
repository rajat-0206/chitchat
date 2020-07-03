from django.contrib import admin

# Register your models here.
from .models import pic,dp,message_save,lastmessage
admin.site.register(pic)
admin.site.register(dp)
admin.site.register(message_save)
admin.site.register(lastmessage)
