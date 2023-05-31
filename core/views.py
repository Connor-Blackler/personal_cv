from django.shortcuts import render, redirect
from .models import GitRepo, Language


def home_page(request):
    context = {"repos": GitRepo.objects.all()}

    return render(request, "home-page.html", context)
