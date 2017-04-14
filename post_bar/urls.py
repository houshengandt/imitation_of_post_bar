from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.TestView.as_view(), name='test'),
    url(r'^sign-in/$', views.SignInView.as_view(), name="sign-in"),
    url(r'^login/$', views.login_to_system, name="login"),
    url(r'^logout/$', views.logout_off_system, name="logout"),
]