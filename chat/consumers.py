import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import message_save,lastmessage,pic
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
import threading

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        current = datetime.datetime.now()
        date = str(current.month)+"/"+str(current.day)+"/"+str(current.year)
        time= str(current.hour)+":"+str(current.minute)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        naam = text_data_json['name']
        def store(message):
            c_id_in=self.room_name
            m=message_save.objects.create(text=message,cus_id=c_id_in,name=naam,time=time)
            m.save()
            x=c_id_in.index("x")
            room_name1=int(c_id_in[0:x])
            room_name2=int(c_id_in[x+1:])
            name_by_id1=User.objects.get(id=room_name1)
            name_by_id2=User.objects.get(id=room_name2)
            name1=name_by_id1.first_name+" "+name_by_id1.last_name
            u_name1=name_by_id1.username
            name2=name_by_id2.first_name+" "+name_by_id2.last_name
            u_name2=name_by_id2.username
            if naam==name1:
                m_id1=name_by_id1.id
            else:
                m_id1=name_by_id1.id
            if naam==name2:
                m_id2=name_by_id2.id
            else:
                m_id2=name_by_id2.id
            try:
                row=lastmessage.objects.filter(cus_id="http://127.0.0.1:8000/chating/"+c_id_in)
                for x in row:
                    x.delete()
                new=lastmessage.objects.create(myid=name1,fid=name2,cus_id="http://127.0.0.1:8000/chating/"+c_id_in,Uname=u_name1,flag=m_id1,f_id=m_id2,pic_url=pic.objects.get(user_id=m_id2).pic_url)
                new.save()
                new=lastmessage.objects.create(myid=name2,fid=name1,cus_id='http://127.0.0.1:8000/chating/'+c_id_in,Uname=u_name2,flag=m_id2,f_id=m_id1,pic_url=pic.objects.get(user_id=m_id1).pic_url)
                new.save()
            except Exception:
                new=lastmessage.objects.create(myid=name1,fid=name2,cus_id="http://127.0.0.1:8000/chating/"+c_id_in,Uname=u_name1,f_id=m_id2,pic_url=pic.objects.get(user_id=m_id2).pic_url)
                new.save()
                new=lastmessage.objects.create(myid=name2,fid=name1,cus_id='http://127.0.0.1:8000/chating/'+c_id_in,Uname=u_name2,f_id=m_id1,pic_url=pic.objects.get(user_id=m_id1).pic_url)
                new.save()
        t = threading.Thread(target=store, args=(message,))
        t.setDaemon(True)
        t.start()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name' : naam,
                'date' : date,
                'time' : time
            }
        )
        # c_id_in=self.room_name
        # m=message_save.objects.create(text=message,cus_id=c_id_in)
        # m.save()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        naam = event['name']
        time = event['time'],
        date = event['date']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'name' :naam,
            'time':time,
            'date':date
        }))