import uuid
from apps.core.models import TimeRegistryBaseModel
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


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
        "InterestCategory", on_delete=models.CASCADE)
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
    username = None
    email = models.EmailField(unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    verified_status = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, null=True, blank=True)
    preferences_id = models.ForeignKey(
        UserPreferences, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True)  # saves single avatar

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # required when creating

    def __str__(self):
        return self.email


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)  # one-to-many
    # multiple photos for the user
    photos = models.ImageField(upload_to="user_photos/", null=True, blank=True)


class Grade(TimeRegistryBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id_given = models.ManyToManyField(
        "CustomUser", related_name="grades_given")
    user_id_received = models.ManyToManyField(
        "CustomUser", related_name="grades_received")
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
        "Interest", related_name="child_interests")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
