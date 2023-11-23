
from django.urls import path
from apps.chat.consumers import ChatConsumer
 

websocket_urlpatterns = [
    path('ws/<str:roomId>/', ChatConsumer.as_asgi()),
]