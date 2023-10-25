import uuid
from apps.core.models import TimeRegistryBaseModel
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone



class MaritalStatus(models.Model):
    id = models.AutoField(primary_key=True)
    marital_status_name = models.CharField(max_length=30)


class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=10)


class InterestCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)


class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(
        'InterestCategory', on_delete=models.CASCADE)
    interest_name = models.CharField(max_length=50)


class UserPreferences(models.Model):
    id = models.AutoField(primary_key=True)
    parent_age = models.IntegerField()
    parent_gender = models.ForeignKey(
        "Gender", on_delete=models.CASCADE, related_name="parent_gender")
    marital_id = models.ManyToManyField(
        "MaritalStatus", related_name="parent_marital_preference")
    child_age = models.IntegerField()
    child_gender = models.ForeignKey("Gender", on_delete=models.CASCADE)
    child_interest = models.ManyToManyField(
        "Interest", related_name="child_interest")


class UserRatingEnum(models.Model):
    pass


class CustomUser(AbstractUser, PermissionsMixin, TimeRegistryBaseModel):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    verified_status = models.BooleanField(default=False)
    # date_joined = models.DateField(default=timezone.now)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    birthdate = models.DateField()
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE)
    preferences_id = models.ForeignKey(
        UserPreferences, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True)  # saves single avatar

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']  # required when creating

    def __str__(self):
        return self.uuid


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)  # one-to-many
    # multiple photos for the user
    photos = models.ImageField(upload_to='user_photos/', null=True, blank=True)


class Grade(TimeRegistryBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id_given = models.ManyToManyField(
        'CustomUser', related_name='grades_given')
    user_id_received = models.ManyToManyField(
        'CustomUser', related_name='grades_received')
    grade = models.ForeignKey(
        UserRatingEnum, on_delete=models.CASCADE)  # CHECK


class Child(TimeRegistryBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    birthdate = models.DateField()
    gender_id = models.OneToOneField(
        "Gender", on_delete=models.CASCADE, related_name="child_gender")
    bio = models.TextField()
    interest_id = models.ManyToManyField(
        'Interest', related_name='child_interests')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
