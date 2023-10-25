from django.contrib import admin
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ("email", "first_name", "last_name", "bio", "location", "birthdate", "avatar")
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ("email", "first_name", "last_name", "bio", "location", "birthdate", "marital_status", "preferences_id", "avatar", "gender", "marital_status")


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bio", "location", "birthdate", "avatar", "gender")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    ordering = ("email",)


# Register the CustomUser model with the updated admin class
admin.site.register(CustomUser, CustomUserAdmin)