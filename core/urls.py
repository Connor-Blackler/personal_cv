from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('education/', views.education, name="education"),
    path('about-me/', views.about_me, name="about-me"),
]
