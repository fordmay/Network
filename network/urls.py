
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile_page/<str:user_name>", views.profile_page, name="profile_page"),
    path("profile_page/<str:user_name>/followers_list", views.followers_list, name="followers_list"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
