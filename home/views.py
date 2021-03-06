from django.shortcuts import render, redirect
from django.contrib import messages

from pprint import pprint

from projects.models import Project


def home(request):
    if (request.user.is_authenticated):
        user = request.user
        if(user.profile.description == ""):
            messages.error(
                request, 'Your account has no description!')
        user_projects = Project.objects.filter(user=user.profile)
        customer_projects = list(Project.objects.filter(
            participants=user.profile).order_by().distinct())
        for team in user.profile.teams.all():
            customer_projects.append(team.task.project)
        cd = {}
        for customer_project in customer_projects:
            cd[customer_project.id] = customer_project

        customer_projects = cd.values()
        given_offers_projects = Project.objects.filter(
            pk__in=get_given_offer_projects(user)).distinct()
        return render(
            request,
            'index.html',
            {
                'user_projects': user_projects,
                'customer_projects': customer_projects,
                'given_offers_projects': given_offers_projects,
            })
    else:
        return redirect('projects')


def get_given_offer_projects(user):
    project_ids = set()

    for taskoffer in user.profile.taskoffer_set.all():
        project_ids.add(taskoffer.task.project.id)

    return project_ids
