from django import template
from apps.chat.models import Message

register = template.Library()

@register.filter
def last_message(room):
    last_message = Message.objects.filter(room=room).order_by('-created_at').first()
    return last_message

@register.filter
def unread_messages_count(user):
    return Message.objects.filter(recipient=user.profile, is_read=False).count()
