from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_post_bar', views.create_post_bar, name='create_post_bar'),
    url(r'^add_post_bar', views.AddPostBarView.as_view(), name='add_post_bar'),
    url(r'^sign-in/$', views.SignInView.as_view(), name="sign-in"),
    url(r'^login/$', views.login_to_system, name="login"),
    url(r'^logout/$', views.logout_off_system, name="logout"),
]