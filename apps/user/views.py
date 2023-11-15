from typing import Optional
from datetime import date, datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser, Interest
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
    return redirect(user_profile_own)


@login_required
def user_logout(request):
    logout(request)
    return redirect("home_page")


@login_required
def user_profile_own(request):
    children_data = []

    user = request.user

    # Loop through the children
    for child in user.child_set.all():
        child_data = {
            "first_name": child.first_name,
            "gender": child.gender_id.gender_name,
            "age": (date.today() - child.birthdate).days // 365,
            "bio": child.bio,
            "avatar": child.avatar.url if child.avatar else None,
            "interests": ', '.join([interest.interest_name for interest in child.interest_id.all()]),
            "child_images": [picture.picture.url for picture in child.pictures.all()],
        }

        children_data.append(child_data)

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
        "children_data": children_data
    }
    return render(request, "user/user_page_own.html", context)


@login_required
def user_swiping(request):
    userlist = CustomUser.objects.all()
    interestlist = Interest.objects.all()

    context = {
        "userlist": userlist,
        "interestlist": interestlist,
    }

    return render(request, "user/swiping.html", context)

# TODO:user_profile_own edit profile, change profile picture functs
# TODO: make default smth for pages when user must be logged-in, otherwise /profile page fails
