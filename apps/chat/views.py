from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Message, Room
from apps.user.utils import check_mutual_like

from apps.user.models import CustomUser


@login_required(login_url="login")
def inbox(request):
    user = request.user
    rooms = Room.objects.filter(members=user)
    unread_message_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    for room in rooms:
        room.partner = room.get_partner(user)

    context = {
        "rooms": rooms,
        "unread_message_count": unread_message_count,
    }

    return render(request, 'chats/inbox.html', context)


@login_required(login_url="login")
def private_chat_view(request, pk):
    user = request.user
    room = Room.objects.get(uuid=pk)
    other_user = room.get_partner(user)
    chat_messages = room.messages.all().reverse()

    for cm in chat_messages:
        if cm.sender != user:
            cm.is_read = True
            cm.save()
        
    return render(request, 'chats/room.html', {
        'chat_messages': chat_messages,
        'room': room,
        'user': user,
        'other_user': other_user
    })

    