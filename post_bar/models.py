# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("用户名", max_length=32, unique=True)
    email = models.EmailField("邮箱", unique=True)
    avatar = models.ImageField("头像", upload_to='avatars/', default='media/avatars/default.jpg')
    last_login = models.DateTimeField("上次登录时间", blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField("用户状态", default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.username + self.email

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username


class PostBar(models.Model):
    bar_name = models.CharField("贴吧名称", max_length=32)
    creator = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='created_bar')
    manager = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, related_name='managing_bar')
    create_time = models.DateTimeField("贴吧创建时间", auto_now_add=True)

    def __unicode__(self):
        return self.bar_name


class Post(models.Model):
    bar = models.ForeignKey(to='PostBar', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField("帖子标题", max_length=32)
    poster = models.OneToOneField(to='User', on_delete=models.CASCADE, related_name='posted')
    content = models.TextField("帖子内容")
    create_time = models.DateTimeField("发帖时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField("评论内容")
    comment_time = models.DateTimeField("评论时间", auto_now_add=True)
    commenter = models.OneToOneField(to='User')
    child_comment = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE, related_name='father_comment')
