from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('',views.home,name="home"),
    path('chating/<str:room_name>/', views.room, name='room'),
    path('eval/<str:room_url>/', views.evaluate, name='evaluate'),
    path('updated/<str:url>/', views.update_dp, name='update_dp'),
    path('videocall/<str:room_name>/', views.videoCall, name='videocall'),
    path('video_call_cut/<str:room_name>/', views.video_call_cut, name='video_call_cut'),
    path('acceptvc/<str:u_id>/', views.acceptvc, name='videocall'),
    path('status/<str:room_name>/', views.vcstatus, name='videostatus'),
    path('block/<str:room>/', views.blockUser, name='block'),
    path('unblock/<str:room>/', views.unblockuser, name='unblock'),
    path('login',views.login_page,name="login_page"),
    path('user_login',views.user_login,name="user_login"),
    path('signup',views.signup_page,name="signup_page"),
    path('register',views.register,name="register"),
    path('chan',views.change_name,name="change_name"),
    path('rajat',views.rajat,name="register"),
    path('user_logout', views.user_logout, name='user_logout'),
    path('latest', views.latest, name="latest"),
    path('change_name', views.change_name, name="Name Change"),
    path('change_pass', views.change_pass, name="Pass Change"),
    path('del_dp', views.del_dp, name="DP Change"),
    path('delete_account', views.delete_account, name="Account Deleted"),
    path('manifest.json',views.manifest,name="manifest"),
    path('offline.html',views.offline,name='offline'),
    path('save_message',views.save_message,name='save_message'),
    path('show_message',views.show_message,name='show_message'),
    path('password',views.forgot,name='forgot'),
    path('enteremail',views.enteremail,name='enteremail'),
    path('forgot_change_pass',views.sendemail,name='sendemail'),
    path('passwordurl',views.change_pass_confirm,name='change_pass_confirm')
    # path('serviceworker.js', (TemplateView.as_view(template_name="chat/serviceworker.js", content_type='application/javascript', )), name='sw.js'),
    # path('OneSignalSDKUpdaterWorker.js', (TemplateView.as_view(template_name="chat/OneSignalSDKUpdaterWorker.js", content_type='application/javascript', )), name='OneSignalSDKUpdaterWorker.js'),
    # path('OneSignalSDKWorker.js', (TemplateView.as_view(template_name="chat/OneSignalUpdaterWorker.js", content_type='application/javascript', )), name='OneSignalWorker.js'),

]
