from django.db import models
from django.utils import timezone


class TimeRegistryBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    # auto create datetime and set editable = False
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
