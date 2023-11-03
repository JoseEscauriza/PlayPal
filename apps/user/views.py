from typing import Optional

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .forms import CustomAuthenticationForm

# Create your views here.


def login_view(request):
    error_message = None
    # Unbound form
    form = CustomAuthenticationForm()
    # Bound form
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        # Validate
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email, password)

            # Authenticate the user
            user: Optional[CustomUser] = authenticate(
                request,
                email=email,
                password=password,
            )
            print(user)

            if user is not None:
                login(request, user)
                return redirect('logged_view')  # TODO: redirect
            else:
                error_message = 'Incorrect email or password. Please try again.'

    context = {'form': form, 'error_message': error_message}

    return render(request, "user/login.html", context)


@login_required
def logged_view(request):
    return render(request, "user/logged_user.html")
