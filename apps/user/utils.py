from datetime import date, timedelta
from typing import Optional

from apps.chat.models import Room, Message
from django.db import transaction, IntegrityError


def calculate_birthdate_from_age(age: str) -> Optional[date]:
    if age is not None:
        today = date.today()
        birthdate = today - timedelta(days=365 * int(age))
        return birthdate
    return None


def check_mutual_like(self, other):
    if other.liked_users.filter(uuid=self.uuid).exists():
        if not Room.objects.filter(members=self).filter(members=other):
            try:
                with transaction.atomic():
                    room = Room.objects.create()
                    room.members.add(self, other)

                    Message.objects.create(
                        room=room,
                        content=f"Great, you matched! Why not send a nice message?"
                    )

            except IntegrityError as e:
                print(f"Integrity Error: {e}")
                raise e

            except Exception as e:
                print(f"Exception raised: {e}")
                raise e