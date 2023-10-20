from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from enum import Enum


class GenderEnum(Enum):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'


class UserRatingEnum(Enum):
    pass


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=2, choices=[(tag, tag.value) for tag in GenderEnum])
    email = models.EmailField(unique=True)
    verified_status = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    bio = models.TextField()
    location = models.TextField()
    birthdate = models.DateField()
    preferences = models.CharField(max_length=500, blank=True)  # CHECK
    last_login = models.DateTimeField(null=True, blank=True)
    staff_status = models.BooleanField(default=False)
    active_status = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # saves single avatar
    groups = models.TextField()
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender', 'date_joined']  # required when creating

    def __str__(self):
        return self.username


class UserPhoto(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # one-to-many
    photos = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # multiple photos for the user


class GenderInterest(models.Model):
    id = models.AutoField(primary_key=True)
    user_account_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # one-to-one
    gender_id = models.CharField(max_length=255, choices=[(tag, tag.value) for tag in GenderEnum])


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    user_id_given = models.ManyToManyField('CustomUser', related_name='grades_given')
    user_id_received = models.ManyToManyField('CustomUser', related_name='grades_received')
    grade = models.CharField(max_length=255, choices=[(rating, rating.value) for rating in UserRatingEnum])  # CHECK


class Children(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    interests = models.CharField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


