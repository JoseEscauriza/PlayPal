from django.db import models


class CreatedModifiedDateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)  # auto create datetime and set editable = False

    class Meta:
        abstract = True