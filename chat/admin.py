from django.contrib import admin

# Register your models here.
from .models import pic,dp,lastmessage
admin.site.register(pic)
admin.site.register(dp)
admin.site.register(lastmessage)
