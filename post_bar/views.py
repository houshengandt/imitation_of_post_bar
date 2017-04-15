# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, PostBar, Post


class TestView(TemplateView):
    template_name = 'post_bar/test.html'


def index(request):
    bars = PostBar.objects.all().order_by('-pk')[:10]
    return render(request, 'post_bar/index.html', {'bars': bars})


@login_required()
def add_post_bar(request):
    return render(request, 'post_bar/add-post-bar.html')


def create_post_bar(request):
    if request.method == 'POST':
        bar_name = request.POST['bar_name']
        creator = request.user
        manager = request.user
        new_post_bar = PostBar(bar_name=bar_name, creator=creator, manager=manager)
        new_post_bar.save()
        return redirect('index')


def bar_detail(request, post_bar_pk):
    post_bar = PostBar.objects.get(pk=post_bar_pk)
    posts = Post.objects.filter(bar=post_bar)
    return render(request, 'post_bar/bar-detail.html', {'post_bar': post_bar, 'posts': posts})


def create_post(request):
    if request.method == 'POST':
        bar = PostBar.objects.get(pk=request.POST['bar_pk'])
        title = request.POST['title']
        content = request.POST['content']
        poster = request.user

        new_post = Post(bar=bar, title=title, content=content, poster=poster)
        new_post.save()

    return redirect('index')   # 跳转到帖子详情页


class SignInView(TemplateView):
    template_name = 'post_bar/sign-in.html'


class SignUpView(TemplateView):
    template_name = 'post_bar/sign-up.html'


def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    try:
        new_user = User.objects.create_user(username, email, password)
        # login(request, new_user)    在这里是对的
    except ValueError:
        pass
    login(request, new_user)
    return redirect('index')


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
