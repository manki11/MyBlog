from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.urls import reverse

from .forms import UserLoginForm


# Create your views here.

def login_view(request):
    form= UserLoginForm(request.POST or None)
    print(request.user.is_authenticated)

    if form.is_valid():
        username= form.cleaned_data.get('username')
        password= form.cleaned_data.get('password')
        user= authenticate(username=username, password=password)
        login(request,user)
        print(request.user.is_authenticated)

    return render(request, "accounts/auth_form.html", {"form": form, "tittle":"Login"})


def register_view(request):
    return render(request, "accounts/auth_form.html", {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:list'))
