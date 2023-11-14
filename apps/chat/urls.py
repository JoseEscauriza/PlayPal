from django.urls import path
from apps.chat import views
 
 
urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("room/<str:pk>", views.private_chat_view, name="room"),
]
