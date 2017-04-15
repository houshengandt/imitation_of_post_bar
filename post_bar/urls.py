from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_post_bar', views.create_post_bar, name='create_post_bar'),
    url(r'^post_bar/(?P<post_bar_pk>\d+)', views.bar_detail, name='bar_detail'),
    url(r'^add_post_bar', views.add_post_bar, name='add_post_bar'),
    url(r'^sign-in/$', views.SignInView.as_view(), name="sign-in"),
    url(r'^sign-up/$', views.SignUpView.as_view(), name="sign-up"),
    url(r'^create-user/$', views.create_user, name="create-user"),
    url(r'^login/$', views.login_to_system, name="login"),
    url(r'^logout/$', views.logout_off_system, name="logout"),
]