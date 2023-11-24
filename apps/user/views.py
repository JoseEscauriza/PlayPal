import uuid
from typing import Optional
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.http import JsonResponse

from .models import CustomUser, Interest, Child
from .forms import CustomAuthenticationForm
from .utils import calculate_birthdate_from_age


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
    # Fetch all interests
    interest_list = Interest.objects.all()

    if request.method == 'POST':
        # Accessing a specific variable from the POST data
        parent_min_age = calculate_birthdate_from_age(request.POST.get('parent-min-age', 18))
        parent_max_age = calculate_birthdate_from_age(request.POST.get('parent-max-age', 70))
        child_min_age = calculate_birthdate_from_age(request.POST.get('child-min-age', 1))
        child_max_age = calculate_birthdate_from_age(request.POST.get('child-max-age', 10))
        interests = request.POST.getlist('interests[]', None)
        rating = request.POST.getlist('rating[]', None)

        # Filter by parent age range
        filtered_users = CustomUser.objects.filter(
            birthdate__gte=parent_max_age,
            birthdate__lte=parent_min_age
        ).prefetch_related(
            'child_set'
        )

        # Exclude users who are in the current user's disliked_users
        disliked_users = request.user.disliked_users.all()
        filtered_users = filtered_users.exclude(uuid__in=disliked_users)

        # Filter by matching child
        matching_users = [
            {
                'user': user,
                'matching_children': user.child_set.filter(
                    birthdate__gte=child_max_age,
                    birthdate__lte=child_min_age,
                    interest_id__interest_name__in=interests
                ).order_by('birthdate').first()
            }
            for user in filtered_users
            if user.child_set.filter(
                birthdate__gte=child_max_age,
                birthdate__lte=child_min_age,
                interest_id__interest_name__in=interests
            ).exists()
        ]

        context = {
            "matching_users": matching_users,
            "interestlist": interest_list
        }
        return render(request, "user/swiping.html", context)

    else:

        # Retrieve all users with at least one child and their first child
        matching_users = CustomUser.objects.filter(child__isnull=False).distinct()

        # Prepare the context with matching users and their first child (if any) and interest for filters
        context = {
            "matching_users": [
                {
                    'user': user,
                    'matching_children': user.child_set.order_by('birthdate').first()
                }
                for user in matching_users
            ],
            "interestlist": interest_list
        }
        return render(request, "user/swiping.html", context)


@login_required
def other_user_profile(request, user_uuid):
    children_data = []

    try:
        user = CustomUser.objects.filter(uuid=user_uuid).first()

        if user is None:
            raise Http404("User not found.")

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
        return render(request, "user/other_user_profile.html", context)

    except ValueError:
        raise Http404("Invalid UUID format.")


def record_action(request):

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        # Assuming user_id is the UUID passed to your function
        user_id = uuid.UUID(user_id)

        # Retrieve the user by UUID
        liked_user = CustomUser.objects.get(uuid=user_id)

        # Record the action based on the provided action parameter
        if action == 'like':
            request.user.liked_users.add(liked_user)
        elif action == 'nope':
            request.user.disliked_users.add(liked_user)

        return JsonResponse({'message': f'User {action}d successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'})

# TODO: swiping html, add check if in liked than card_image_top to liked.png
# TODO: js to show numbers when picking age in filter bar.
# TODO: how to mark liked cards with a symbol or pictire in card ?
# TODO: Maybe we need to add simple:list of liked and disliked users (so you could remove the disliked, once changed your mind or disliked acccidentely)
# TODO:user_profile_own edit profile, change profile picture functs
# TODO: make default smth for pages when user must be logged-in, otherwise /profile page fails

