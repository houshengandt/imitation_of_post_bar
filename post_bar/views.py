# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import User, PostBar, Post, Comment


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


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = Comment.objects.filter(post=post)
    comments_has_not_father = Comment.objects.filter(post=post, father_comment=None)
    comments_has_father = Comment.objects.filter(post=post).exclude(father_comment=None)
    post_bar = post.bar
    content = {'post_bar': post_bar, 'post': post, 'comments': comments, 'comments_has_father': comments_has_father,
               'comments_has_not_father': comments_has_not_father}

    return render(request, 'post_bar/post-detail.html', content)


def add_comment(request):
    if request.method == 'POST':
        post = Post.objects.get(pk=request.POST['post_pk'])
        comment = request.POST['comment']
        parent_comment_pk = request.POST.get('comment_pk')
        commenter = request.user
        if parent_comment_pk:
            parent_comment = Comment.objects.get(pk=parent_comment_pk)
            new_comment = Comment(post=post, comment=comment, commenter=commenter, father_comment=parent_comment)
        else:
            new_comment = Comment(post=post, comment=comment, commenter=commenter)

        new_comment.save()
        # return HttpResponse()
        return redirect('post_deatil', post_pk=post.pk)


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
        login(request, new_user)
    except ValueError:
        pass
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
