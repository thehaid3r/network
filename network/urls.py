
from django.urls import path

from . import views

urlpatterns = [
    path("follow/<str:str>", views.follow, name="follow"),
    path("following/<str:str>", views.following, name="following"),
    path("profile/<str:str>", views.profile, name="profile"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
