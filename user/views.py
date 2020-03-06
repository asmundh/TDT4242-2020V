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
    if(first_name == ""):
        first_name = username
    if(description == ""):
        description = "This user has yet not filled out a description."
    logging.info(username)

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'company': company,
        'city': city,
        'description': description,
        'editing': True
    }
    logging.info(context['editing'])

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user/user_view.html', context=context)


# ...


def edit_desctiption(request, user_id):
    if request.method == 'POST':
        single_profile = get_object_or_404(Profile, pk=user_id)
        username = single_profile.user.username
        company = single_profile.company
        first_name = single_profile.user.first_name
        last_name = single_profile.user.last_name
        city = single_profile.city
        description = single_profile.description
        if(first_name == ""):
            first_name = username
        if(description == ""):
            description = "This user has yet not filled out a description."
        logging.info(username)

        context = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'city': city,
            'description': description,
            'editing': True
        }
        logging.info(context['editing'])
        #single_profile.description = string
        single_profile.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'user/user_view.html', context=context)

# COPY PASTA


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            print()
            request.user.profile.description = form.cleaned_data['description']
            request.user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))
