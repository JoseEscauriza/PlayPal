import uuid

from django.db import models
from apps.core.models import TimeRegistryBaseModel
from django.db.models import Max
from apps.user.models import CustomUser


class Chat(TimeRegistryBaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(CustomUser, related_name='chats')

    def get_partner(self, current_user):
        return self.members.exclude(id=current_user.id).first()

    def get_last_message(self):
        last_message = self.messages.aggregate(
            last_message_time=Max('created_at'))

        if last_message['last_message_time']:
            return self.messages.filter(created_at=last_message['last_message_time']).first()
        else:
            return None

    # def __str__(self):
    #     return self.slug + "_chat"


class Message(TimeRegistryBaseModel):
    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    content = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    read_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created_at',)
