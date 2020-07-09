from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import os
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, authenticate,logout
from .forms import SignUpForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import dp,lastmessage,pic
from django.core.mail import EmailMultiAlternatives,send_mail
import random
import requests
import json
import hashlib, binascii
from django.contrib.sessions.models import Session
import smtplib, ssl
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .models import message_save,lastmessage,changePassword
import hashlib
global logged


def manifest(request):
    return render(request,'chat/manifest.json')

def offline(request):
    return render(request,'chat/offline.html')

def home(request):
    if(request.session.has_key('loged') and request.session['loged']) == True:
        user = User.objects.get(username=request.session['username'])
        m_id = str(user.id)
        logged = User.objects.get(username=request.session['username'])
        allusers = User.objects.all()
        name = user.first_name +" "+user.last_name
        latestmessage=lastmessage.objects.filter(Uname=request.session['username'])[::-1]
        return render(request, 'chat/home.html',{"logged":logged,"users":allusers,"me":user,"Name":name,"latestmessage":latestmessage,"m_id":m_id})
    else:
        return render(request,"chat/base.html")

def rajat(request):
    return render(request,"chat/rajat.html")


def room(request, room_name):
    username = request.session['username']
    user = User.objects.get(username=username)
    logged = User.objects.get(username=username)
    allusers = User.objects.all()
    m_id=str(user.id)

    name = user.first_name +" "+user.last_name
    x=room_name.index("x")
    room_name1=int(room_name[0:x])
    room_name2=int(room_name[x+1:])
    recerror='f'
    if room_name1==user.id or room_name2==user.id:
        try:
            if(room_name1==user.id):
                rec = User.objects.get(id=room_name2)
            else:
                rec = User.objects.get(id=room_name1)
            reciver = rec.first_name +" "+rec.last_name
        except Exception:
            recerror='t'
            rec=dp.objects.get(id=1)
            reciver="Sorry!! User does not exists."
        if room_name1>room_name2:
            r=str(room_name1)+"x"+str(room_name2)
        else:
            r=str(room_2)+"x"+str(room_name1)

        message_save_var=message_save.objects.filter(cus_id=r).order_by('id')
        latestmessage=lastmessage.objects.filter(Uname=username).order_by('id')[::-1]

        for l in latestmessage:

            if l.cus_id=="https://itschitchat.herokuapp.com/chating/"+room_name :
                l.flag='y'
                l.save()

        return render(request, 'chat/room.html', {"logged":logged,"users":allusers,"me":user,'rec':rec,'recerror':recerror,'room_name': room_name,"message_save_var":message_save_var,"Name":name,"Reciever":reciver,"latestmessage":latestmessage,'m_id':m_id})
    else:
        return HttpResponse("You are not authorised to view this page.")
def latest(request):
    username = request.session['username']
    room_name = request.POST['room_name']
    user = User.objects.get(username=username)
    m_id=str(user.id)
    latestmessage=lastmessage.objects.filter(Uname=username).order_by('id')[::-1]
    for l in latestmessage:
        if l.cus_id=="https://itschitchat.herokuapp.com/chating/"+room_name :
            l.flag='y'
            l.save()
    return render(request,'chat/msgcol.html',{"latestmessage":latestmessage,'m_id':m_id})

def evaluate(request, room_url):
    x=room_url.index("x")
    room_url1=int(room_url[0:x])
    room_url2=int(room_url[x+1:])
    if room_url1>room_url2:
        r=str(room_url1)+"x"+str(room_url2)
        return redirect('https://itschitchat.herokuapp.com/chating/'+r)
    else:
        r=str(room_url2)+"x"+str(room_url1)
        return redirect('https://itschitchat.herokuapp.com/chating/'+r)

def chat(request,username):
    users=User.objects.all()
    logged=User.objects.get(username=username)
    return render(request, 'chat/chat.html')

def signup_page(request):
    form = SignUpForm()
    return render(request,'chat/register.html',{'form': form})

def login_page(request):
    if(request.session.has_key('loged') and request.session['loged']) == True:
        return redirect('/')
    else:
        return render(request,'chat/login.html')



def user_login(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                logged=User.objects.get(username=username)
                users=User.objects.all()
                request.session['loged'] = True
                request.session['username'] = username
                return redirect('/')
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            error1="invalid login details supplied!"
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return render(request,'chat/login.html',{'error1':error1})
    else:
        return HttpResponse("You don't have access to this url")

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username=request.POST.get('username')

        if "*" not in username and "@" not in username and "." not in username and "&" not in username and "^" not in username and "$" not in username and "#" not in username and "%" not in username and "-" not in username  and "+" not in username and "?" not in username :
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                o=User.objects.get(username=username)
                r=pic.objects.create(user_id=o.id)
                r.save()
                error1="Registered Successfully!! Login to continue."
                return render(request,'chat/login.html',{'error1':error1})
            else:
                return render(request,'chat/register.html',{'form': form})
        else:
            error="Cannot use '.,!,@,#,$,%,^,&,*,-,+' in username"
            return render(request,'chat/register.html',{'form': form, 'error':error})
    else:
        return render(request,'chat/register.html',{'form': form})

        # return HttpResponse("Invalid details")


def user_logout(request):
    logout(request)
    request.session['loged'] = False
    request.session['uesrname'] =""
    return redirect('/login')


"""settings wale functions"""
def change_name(request):
    if request.method=='POST':
        user = User.objects.get(username=request.session['username'])
        first=request.POST.get("first")
        last=request.POST.get("last")
        user.first_name=first
        user.last_name=last
        user.save()
        name = lastmessage.objects.filter(Uname=request.session['username'])
        for l in name:
            print(l.myid)
            l.myid = first+" "+last
            print(l.myid)
            l.save()
        return HttpResponse("Name Changed Succesfully")

def delete_account(request):
    user = User.objects.get(username=request.session['username'])
    user.delete()
    request.session['loged'] = False
    request.session['uesrname'] =""
    return redirect('/login')

def update_dp(request, url):
    user=User.objects.get(username=request.session['username'])
    dp=pic.objects.get(user_id=user.id)
    dp.pic_url="https://itschitchat.pythonanywhere.com/media/media/"+url
    dp.save()
    # name = user.first_name +" "+user.last_name
    last=lastmessage.objects.filter(f_id=user.id)
    for l in last:
        l.pic_url="https://itschitchat.pythonanywhere.com/media/media/"+url
        l.save()
    return redirect("/")

def del_dp(request):
    user=User.objects.get(username=request.session['username'])
    dp=pic.objects.get(user_id=user.id)
    dp.pic_url="https://itschitchat.pythonanywhere.com/media/media/default.png"
    dp.save()
    # name = user.first_name +" "+user.last_name
    last=lastmessage.objects.filter(f_id=user.id)
    for l in last:
        l.pic_url="https://itschitchat.pythonanywhere.com/media/media/default.png"
        l.save()
    return redirect("/")
def change_pass(request):
    user=User.objects.get(username=request.session['username'])
    current= request.POST.get("current")
    password1= request.POST.get("newone")
    if authenticate(username=request.session['username'],password=current):
        user.set_password(password1)
        user.save()
        return HttpResponse("Password Changed Succesfully")
    else:
        return HttpResponse("Password does not macth")
# https://itschitchat.pythonanywhere.com/media/media/default.png
# default
def show_message(request):
    r=request.POST.get("room_name")
    username = request.session['username']
    user = User.objects.get(username=username)
    # message_save_var=message_save.objects.filter(cus_id=r)
    message_save_var=message_save.objects.filter(cus_id=r).order_by('id')
    return render(request,'chat/show_message.html',{"message_save_var":message_save_var,"me":user})


def save_message(request):
        c_id_in=request.POST.get("room_name")
        message=request.POST.get("message")
        naam=request.POST.get("name")
        time=request.POST.get("time")
        m=message_save.objects.create(text=message,cus_id=c_id_in,name=naam,time=time)
        m.save()
        # u=request.session['username']
        # name_notify=u.first_name+" "+u.last_name
        x=c_id_in.index("x")
        room_name1=int(c_id_in[0:x])
        room_name2=int(c_id_in[x+1:])
        name_by_id1=User.objects.get(id=room_name1)
        name_by_id2=User.objects.get(id=room_name2)
        name1=name_by_id1.first_name+" "+name_by_id1.last_name
        u_name1=name_by_id1.username
        name2=name_by_id2.first_name+" "+name_by_id2.last_name
        u_name2=name_by_id2.username
        if(u_name2==request.session['username']):
            recipient = u_name1
        else:
            recipient = u_name2
        if naam==name1:
            m_id1=name_by_id1.id
        else:
            m_id1=name_by_id1.id
        if naam==name2:
            m_id2=name_by_id2.id
        else:
            m_id2=name_by_id2.id
        try:
            row=lastmessage.objects.filter(cus_id="https://itschitchat.herokuapp.com/chating/"+c_id_in)
            for x in row:
                x.delete()
            new=lastmessage.objects.create(myid=name1,fid=name2,cus_id="https://itschitchat.herokuapp.com/chating/"+c_id_in,Uname=u_name1,flag=m_id1,f_id=m_id2,pic_url=pic.objects.get(user_id=m_id2).pic_url)
            new.save()
            new=lastmessage.objects.create(myid=name2,fid=name1,cus_id='https://itschitchat.herokuapp.com/chating/'+c_id_in,Uname=u_name2,flag=m_id2,f_id=m_id1,pic_url=pic.objects.get(user_id=m_id1).pic_url)
            new.save()
        except Exception:
            new=lastmessage.objects.create(myid=name1,fid=name2,cus_id="https://itschitchat.herokuapp.com/chating/"+c_id_in,Uname=u_name1,f_id=m_id2,pic_url=pic.objects.get(user_id=m_id2).pic_url)
            new.save()
            new=lastmessage.objects.create(myid=name2,fid=name1,cus_id='https://itschitchat.herokuapp.com/chating/'+c_id_in,Uname=u_name2,f_id=m_id1,pic_url=pic.objects.get(user_id=m_id1).pic_url)
            new.save()
        header = {"Content-Type":"application/json; charset=utf-8","Authorization": "Basic NGQ1NDJmZmYtYjc2ZS00YTA5LThlZDMtYzA0MzQ3YTBhYjU1"}
        payload = {"app_id":"56f464d8-5f40-479c-b005-7bbc1dff146d","include_external_user_ids":[recipient],"contents":{"en":"You have recieved a new message from "+naam},"headings":{"en":"Chitchat"},"url":"https://itschitchat.herokuapp.com/chating/"+c_id_in,"chrome_web_icon":"https://itschitchat.pythonanywhere.com/media/media/"+naam+".jpg","chrome_web_badge":"https://itschitchat.herokuapp.com/static/images/icon-192x192.png"}
        print(payload)
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(req.status_code, req.reason,req.text,sep="----000----")
        return HttpResponse("Sent")
def enteremail(request):
    email=request.POST.get('email')
    s=User.objects.filter(email=email)
    if s:
        error=""
    else:
        error="No user with this email exists"
    return render(request,'chat/account_confirm.html',{"acc":s,"error":error})
def forgot(request):
    return render(request,'chat/password_reset.html')

def sendemail(request,name_pass):
    subject = 'Change password for ChitChat'
    hash_object = hashlib.md5(name_pass.encode())
    sendlink=hash_object.hexdigest()
    u=User.objects.get(username=name_pass)
    messages = "Hi!!"+"\n"+"Here is the link to change your password"+"\n"+"https://itschitchat.herokuapp.com/passwordurl/"+sendlink
    hashsave=changePassword.objects.create(token=sendlink,u_name=u.username)
    recepient =u.email
    print(recepient)
    send_mail(subject,
        messages, EMAIL_HOST_USER, [recepient])
    error="Link to change password is sent to your mail."
    return render(request ,'chat/error.html',{'error':error})

def change_pass_confirm(request,url_token):
    if request.method=='POST':
        if changePassword.objects.get(token=url_token):
            s=changePassword.objects.get(token=url_token)
            name=s.u_name
            user=User.objects.get(username=name)
            password1= request.POST.get("pass1")
            password2= request.POST.get("pass2")
            if password1==password2 and len(password1)>=8:
                user.set_password(password1)
                user.save()
                s.delete()
                error="Password Changed Succesfully.Login to continue."
                return render(request ,'chat/error.html',{'error':error})
            else:
                error="Either password is less than 8 digits or password did not match with confirm password"
                return render(request,'chat/password_reset_form.html',{'url':url_token,'error':error})
        else:
            return HttpResponse("Sorry you can't access the page. Please contact admin")
    else:
        return render(request,'chat/password_reset_form.html',{'url':url_token})
