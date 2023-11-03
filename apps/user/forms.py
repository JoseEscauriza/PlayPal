from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """ Redefines base UserCreationForm with CustomUser fields (no username)"""
    email = forms.EmailField(required=True)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True) -> CustomUser:
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """ Redefines base UserCreationForm with CustomUser fields"""

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "bio",
            "location",
            "birthdate",
            "marital_status",
            "avatar",
            "gender",
            "marital_status")
