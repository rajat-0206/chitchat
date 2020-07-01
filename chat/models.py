from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class message_save(models.Model):
    text=models.TextField()
    cus_id=models.CharField(max_length=500)
    name = models.CharField(max_length = 500,default='unavailable')
    date = models.CharField(max_length=30,default='6/26/2020')
    time = models.TextField(max_length=10,default="12:00")

class dp(models.Model):
    name=models.CharField(max_length=500)
    pic_url=models.CharField(max_length=10000,default='http://itschitchat.pythonanywhere.com/media/media/default.png')

class lastmessage(models.Model):
    myid = models.CharField(max_length=200)
    fid= models.CharField(max_length=200)
    cus_id=models.CharField(max_length=500)
    pic_url=models.CharField(max_length=10000,default='http://itschitchat.pythonanywhere.com/media/media/default.png')
    pic_url=models.CharField(max_length=500,default='http://itschitchat.pythonanywhere.com/media/media/default.png')
    f_id=models.CharField(max_length=500, default='a')
    Uname=models.CharField(max_length=500,default='#')
    flag=models.CharField(max_length=500, default='x')

class pic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic_url=models.CharField(max_length=500,default='http://itschitchat.pythonanywhere.com/media/media/default.png')
