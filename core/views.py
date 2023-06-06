from django.shortcuts import render, redirect
from .models import GitRepo, Language, Education


def home_page(request):
    context = {"repos": GitRepo.objects.all()}

    return render(request, "home-page.html", context)


def education(request):
    education_complete = Education.objects.filter(state='Completed')
    education_in_progress = Education.objects.filter(state='In-progress')
    education_not_started = Education.objects.filter(state='Not-started')

    context = {
        "education_complete": education_complete,
        "education_in_progress": education_in_progress,
        "education_not_started": education_not_started,
    }

    return render(request, "education.html", context)


def about_me(request):
    context = {}

    return render(request, "about-me.html", context)
