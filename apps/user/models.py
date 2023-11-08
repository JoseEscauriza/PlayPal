import uuid
from typing import List

from django.db import models
from apps.core.models import TimeRegistryBaseModel
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User

from apps.user import validators


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password=None, **extra_fields) -> User:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password=None, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class MaritalStatus(models.Model):
    id = models.AutoField(primary_key=True)
    marital_status = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Marital statuses"

    def __str__(self) -> str:
        return self.marital_status


class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.gender_name


class InterestCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Interest categories"

    def __str__(self) -> str:
        return self.category_name


class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(
        "InterestCategory", on_delete=models.CASCADE)
    interest_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.interest_name


class UserPreference(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        "CustomUser", on_delete=models.CASCADE, related_name="preferences")
    parent_lower_age_range = models.IntegerField()
    parent_upper_age_range = models.IntegerField()
    parent_gender = models.ManyToManyField(
        "user.Gender", related_name="parent_gender_preference")
    marital_id = models.ManyToManyField(
        "MaritalStatus", related_name="parent_marital_preference")
    child_lower_age_range = models.IntegerField()
    child_upper_age_range = models.IntegerField()
    child_gender = models.ManyToManyField(
        "Gender", related_name="child_gender_preference")
    child_interest = models.ManyToManyField(
        "Interest", related_name="child_interest")

    def __str__(self) -> str:
        return f"ID: {self.id}"


class CustomUser(AbstractUser, PermissionsMixin, TimeRegistryBaseModel):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    verified_status = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []  # TODO: think thoroughly what we actually-required when creating a user

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        """ Does the user have a specific permission? """
        return True


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to="user_photos/", null=True, blank=True)


class Grade(TimeRegistryBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id_given = models.ManyToManyField(
        "CustomUser", related_name="grades_given")
    user_id_received = models.ManyToManyField(
        "CustomUser", related_name="grades_received")
    grade = models.IntegerField(validators=[validators.check_rating_range])


class Child(TimeRegistryBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    birthdate = models.DateField()
    gender_id = models.OneToOneField(
        "Gender", on_delete=models.CASCADE, related_name="child_gender")
    bio = models.TextField()
    interest_id = models.ManyToManyField(
        "Interest", related_name="child_interests")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Children"

    def __str__(self) -> str:
        return self.first_name


class ChildPicture(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='child_pictures/')

    def __str__(self):
        return f"Picture for {self.child.first_name}"
