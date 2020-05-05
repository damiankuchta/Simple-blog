from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from . import models

def register(request):
    if request.POST:

        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            models.UserProfile(user=user).save()
            login(request, user)
    else:
        user_creation_form = UserCreationForm()

    return render(request, "auth_app/register.html", {"user_creation_form": user_creation_form})
