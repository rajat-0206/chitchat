from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
channel_routing = {
    'websocket.connect': consumers.ChatConsumer.connect,
    'websocket.receive': consumers.ChatConsumer.receive,
    'websocket.disconnect': consumers.ChatConsumer.disconnect,
}
