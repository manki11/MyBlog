from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm


# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        response = HttpResponse("You are already logged in!!")
        response.status_code = 403
        return response
    next= request.GET.get('next')

    form = UserLoginForm(request.POST or None)
    print(request.user.is_authenticated)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated)
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('posts:list'))

    return render(request, "accounts/auth_form.html", {"form": form, "tittle": "Login"})


def register_view(request):
    if request.user.is_authenticated:
        response = HttpResponse("You are already logged in!!")
        response.status_code = 403
        return response
    next= request.GET.get('next')

    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('posts:list'))

    return render(request, "accounts/auth_form.html", {"form": form, "tittle": "Register"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:list'))
