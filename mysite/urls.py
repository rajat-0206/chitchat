
from django.contrib import admin
from django.urls import path,include
from  chat import views


urlpatterns = [
    path('',include('chat.urls')),
    path('admin/', admin.site.urls),
    path('',include('pwa.urls')),


]
