from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from ..forms.auth import UserRegisterForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, "store/login.html", {"form": form})


def register(request):
    form = UserRegisterForm()
    return render(request, "store/register.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect("home")
    else:
        user_form = UserRegisterForm()
    return render(
        request,
        "store/register.html",
        {"user_form": user_form},
    )
