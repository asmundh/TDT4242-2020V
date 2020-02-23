import logging.config
import sys
from django.http import HttpResponse
from projects.models import ProjectCategory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm, user_view_form
from user.models import Profile

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

    logging.info(username)
    logging.info(company)
    logging.info(first_name)
    logging.info(last_name)
    logging.info(city)

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'company': company,
        'city': city
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user/user_view.html', context=context)
