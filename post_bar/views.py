# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone

from .models import PostBar


class TestView(TemplateView):
    template_name = 'post_bar/test.html'


def index(request):
    bars = PostBar.objects.all().order_by('-pk')[:10]
    return render(request, 'post_bar/index.html', {'bars': bars})


class AddPostBarView(TemplateView):
    template_name = 'post_bar/add-post-bar.html'


def create_post_bar(request):
    if request.method == 'POST':
        bar_name = request.POST['bar_name']
        creator = request.user
        manager = request.user
        new_post_bar = PostBar(bar_name=bar_name, creator=creator, manager=manager)
        new_post_bar.save()
        return redirect('index')


class SignInView(TemplateView):
    template_name = 'post_bar/sign-in.html'


def login_to_system(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user and user.is_active:
            login(request, user)
    return redirect('index')


def logout_off_system(request):
    logout(request)
    return redirect('index')

