import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from enum import Enum


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
    category_id = models.ForeignKey('InterestCategory', on_delete=models.CASCADE)
    interest_name = models.CharField(max_length=50)


class UserPreferences(models.Model):
    id = models.AutoField(primary_key=True)
    parent_age = models.IntegerField()
    parent_gender = models.ForeignKey("Gender", on_delete=models.CASCADE)
    marital_id = models.ManyToManyField("MaritalStatus", related_name="parent_marital_preference")
    child_age = models.IntegerField()
    child_gender = models.ForeignKey("Gender", on_delete=models.CASCADE)
    child_interest = models.ManyToManyField("Interest", related_name="child_interests")


class UserRatingEnum(Enum):
    pass


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender_id = models.IntegerField()
    verified_status = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    birthdate = models.DateField()
    marital_id = models.IntegerField()
    preferences_id = models.IntegerField()
    staff_status = models.BooleanField(default=False)
    active_status = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # saves single avatar
    # groups = models.TextField()
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender_id']  # required when creating

    def __str__(self):
        return self.username


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # one-to-many
    photos = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # multiple photos for the user


class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id_given = models.ManyToManyField('CustomUser', related_name='grades_given')
    user_id_received = models.ManyToManyField('CustomUser', related_name='grades_received')
    grade = models.CharField(max_length=255, choices=[(rating, rating.value) for rating in UserRatingEnum])  # CHECK


class Child(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    birthdate = models.DateField()
    gender_id = models.OneToOneField("Gender", on_delete=models.CASCADE, related_name="child_gender")
    bio = models.TextField()
    interest_id = models.ManyToManyField('Interest', related_name='child_interests')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


# TODO: Create separate CREATED_AT / MODIFIED_AT to be inherited from
# TODO: Check location django field options
