from typing import Optional

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from .forms import CustomAuthenticationForm


def login_view(request):
    error_message = None
    form = CustomAuthenticationForm()

    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user: Optional[CustomUser] = authenticate(
                request,
                email=email,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("logged_view")
            else:
                error_message = "Incorrect email or password. Please try again."

    context = {"form": form, "error_message": error_message}

    return render(request, "user/login.html", context)


@login_required
def logged_view(request):
    return render(request, "user/logged_user.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home_page")


@login_required
def user_profile_own(request):
    user = request.user
    context = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "verified_status": user.verified_status,
        "bio": user.bio,
        "location": user.location,
        "birthdate": user.birthdate,
        "marital_status": user.marital_status,
        "avatar": user.avatar.url if user.avatar else None,
    }
    return render(request, "user/user_page_own.html", context)
