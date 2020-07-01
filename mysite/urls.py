
from django.contrib import admin
from django.urls import path,include
from  chat import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',include('chat.urls')),
    path('admin/', admin.site.urls),
    

]
