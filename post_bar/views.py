# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

import os, json

from .models import User, PostBar, Post, Comment, Notification


class TestView(TemplateView):
    template_name = 'post_bar/test.html'


def index(request):
    bars = PostBar.objects.all().order_by('-pk')[:10]
    return render(request, 'post_bar/index.html', {'bars': bars})


def add_post_bar(request):
    return render(request, 'post_bar/add-post-bar.html')


@login_required()
def create_post_bar(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        cover = request.FILES.get("cover", None)
        bar_name = request.POST['bar_name']
        description = request.POST['description']
        creator = request.user
        manager = request.user
        (shotname, extension) = os.path.splitext(cover.name)
        cover.name = str(creator.pk) + extension
        new_post_bar = PostBar(bar_name=bar_name, cover=cover, description=description, creator=creator, manager=manager)
        new_post_bar.save()
        return redirect('index')


def enter_or_create(request):
    if request.method == 'POST':
        bar_name = request.POST['bar_name']
        try:
            bar = PostBar.objects.get(bar_name=bar_name)
        except PostBar.DoesNotExist:
            messages.info(request, "还没有 %s 这个贴吧， 马上创建" % bar_name)
            return redirect('add_post_bar')
        return redirect('bar_detail', post_bar_pk=bar.pk)


def bar_detail(request, post_bar_pk):
    post_bar = PostBar.objects.get(pk=post_bar_pk)
    posts = Post.objects.filter(bar=post_bar).order_by('-update_time')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    page_nums = paginator.page_range
    return render(request, 'post_bar/bar-detail.html', {'post_bar': post_bar, 'posts': contacts, 'page_nums': page_nums})


@login_required()
def create_post(request):
    if request.method == 'POST':
        bar = PostBar.objects.get(pk=request.POST['bar_pk'])
        title = request.POST['title']
        content = request.POST['content']
        poster = request.user

        new_post = Post(bar=bar, title=title, content=content, poster=poster)
        new_post.save()

    return redirect('post_detail', post_pk=new_post.pk)


@login_required()
def delete_post(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        pass
    if request.user == post.poster:
        post.delete()
        return redirect('bar_detail', post_bar_pk=post.bar.pk)
    else:
        return HttpResponse(status=403)


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = Comment.objects.filter(post=post)
    comments_has_not_father = Comment.objects.filter(post=post, father_comment=None).order_by('-comment_time')
    comments_has_father = Comment.objects.filter(post=post).exclude(father_comment=None)
    paginator = Paginator(comments_has_not_father, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    page_nums = paginator.page_range
    post_bar = post.bar
    content = {'post_bar': post_bar, 'post': post, 'comments_has_father': comments_has_father,
               'comments_has_not_father': contacts, 'page_nums': page_nums}

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
        post.update_time = timezone.now()
        post.save()
        new_comment.save()

        new_notification = Notification(receiver=post.poster, trigger=request.user, action_content=new_comment)
        new_notification.save()
        # return HttpResponse()
        if request.is_ajax():
            response_content = '<li class="comment-list-item list-group-item"><p><a href="%s">' \
                               '你</a> 回复 <a href="%s">' \
                               '%s</a>:<p>%s</p><div class="comment-info"><a href="%s">删除</a></div></li>'
            response_content = response_content % (commenter.get_absolute_url(), parent_comment.commenter.get_absolute_url(),
                                                   parent_comment.commenter.username, comment, '/delete_comment/' + str(new_comment.pk))
            print(response_content)
            return HttpResponse(response_content)
        else:
            return redirect('post_detail', post_pk=post.pk)


@login_required()
def delete_comment(request, comment_pk):
    try:
        comment = Comment.objects.get(pk=comment_pk)
    except Comment.DoesNotExist:
        pass
    if request.user == comment.commenter or request.user == comment.post.poster:
        comment.delete()
        return redirect('post_detail', post_pk=comment.post.pk)
    else:
        return HttpResponse(status=403)


class SignInView(TemplateView):
    template_name = 'post_bar/sign-in.html'


def sign_in(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'post_bar/sign-in.html')

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
    next_url = request.POST.get('next')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user and user.is_active:
            login(request, user)
    return redirect(request.session['login_from'])


def logout_off_system(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def profile(request, user_pk):
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        pass
    return render(request, 'post_bar/profile.html', {'this_user': user})


def get_notification(request):
    notifications = Notification.objects.filter(receiver=request.user, unread=True)
    noti = []
    for notification in notifications:
        n = {'trigger': notification.trigger.username, 'trigger_id': notification.trigger.pk,
             'action_content': notification.action_content.comment, 'action_content_id': notification.action_content.pk}
        noti.append(n)
    noti = json.dumps(noti)
    return HttpResponse(noti)


def mark_all_as_read(request):
    notifications = Notification.objects.filter(receiver=request.user)
    for notification in notifications:
        notification.mark_as_read()
    return HttpResponse()
