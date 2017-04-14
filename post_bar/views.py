# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone


class TestView(TemplateView):
    template_name = 'post_bar/test.html'


class SignInView(TemplateView):
    template_name = 'post_bar/sign-in.html'


def login_to_system(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user and user.is_active:
            login(request, user)
    return redirect('test')


def logout_off_system(request):
    logout(request)
    return redirect('test')

