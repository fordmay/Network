from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .forms import PostForm
from .models import User, Post


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            content_form = form.save(commit=False)
            content_form.owner = request.user
            content_form.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "network/index.html", {
        "title": "All Posts",
        "form": PostForm(),
        "posts": pagination(request, Post.objects.order_by("time").reverse())
    })


def profile_page(request, user_name):
    if User.objects.filter(username=user_name).exists():
        return render(request, "network/index.html", {
            "title": "Profile Page",
            "user_info": User.objects.get(username=user_name),
            "posts": pagination(request, Post.objects.filter(owner__username=user_name).order_by("time").reverse())
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")


@login_required(login_url="/login")
def followers_list(request, user_name):
    # Follow and Unfollow
    if request.method == "POST":
        user = User.objects.get(username=user_name)
        if request.user.follows.filter(username=user_name).exists():
            request.user.follows.remove(user)
        else:
            request.user.follows.add(user)
    return HttpResponseRedirect(reverse("profile_page", args=(user_name,)))


@login_required(login_url="/login")
def following(request):
    return render(request, "network/index.html", {
        "title": "Following",
        "posts": pagination(request,
                            Post.objects.filter(owner__in=request.user.follows.all()).order_by("time").reverse())
    })


def pagination(request, objects):
    paginator = Paginator(objects, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
