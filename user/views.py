import logging.config
import sys
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import ProjectCategory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import SignUpForm
from user.models import Profile
from .forms import UpdateProfile

import logging

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


def index(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.company = form.cleaned_data.get('company')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.postal_code = form.cleaned_data.get('postal_code')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.street_address = form.cleaned_data.get('street_address')
            user.profile.description = form.cleaned_data.get('description')
            user.profile.company = form.cleaned_data.get('company')
            user.is_active = False

            user.profile.categories.add(*form.cleaned_data['categories'])
            user.save()
            # TODO - fix raw_password
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)

            messages.success(
                request, 'Your account has been created and is awaiting verification.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


def user_view(request, user_id):

    single_profile = get_object_or_404(
        Profile, user__username=user_id)

    username = single_profile.user.username
    company = single_profile.company
    first_name = single_profile.user.first_name
    last_name = single_profile.user.last_name
    city = single_profile.city
    description = single_profile.description
    email_notifications = single_profile.email_notifications
    get_average_rating = single_profile.get_average_rating
    get_rating_count = single_profile.get_rating_count
    if(first_name == ""):
        first_name = username
    if(description == ""):
        description = "This user has yet not filled out a description."

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'company': company,
        'city': city,
        'description': description,
        'email_notifications': email_notifications,
        'get_average_rating': get_average_rating,
        'get_rating_count': get_rating_count,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user/user_view.html', context=context)

# COPY PASTA


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user
            #(f"before user: {user.profile.email_notifications}")
            user.profile.description = form.cleaned_data['description']
            user.profile.email_notifications = form.cleaned_data['email_notifications']
            user.save()
            messages.success(
                request, 'Your account has been updated.')
            return redirect('user_view', user.username)
    else:
        messages.error(
            request, 'Your account has not been created and is awaiting verification.')
        return redirect('user_view', user.username)
