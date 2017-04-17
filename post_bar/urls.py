from django.conf.urls import url, static

from . import views
from imitation_of_post_bar import settings


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_post_bar', views.create_post_bar, name='create_post_bar'),
    url(r'^enter_or_create_bar', views.enter_or_create, name='enter_or_create_bar'),
    url(r'^post_bar/(?P<post_bar_pk>\d+)', views.bar_detail, name='bar_detail'),
    url(r'^add_post_bar', views.add_post_bar, name='add_post_bar'),
    url(r'^create_post', views.create_post, name='create_post'),
    url(r'^delete_post/(?P<post_pk>\d+)/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create_comment/$', views.add_comment, name='create_comment'),
    url(r'^delete_comment/(?P<comment_pk>\d+)$', views.delete_comment, name='delete_comment'),
    url(r'^sign-in/$', views.sign_in, name="sign-in"),
    url(r'^sign-up/$', views.SignUpView.as_view(), name="sign-up"),
    url(r'^create-user/$', views.create_user, name="create-user"),
    url(r'^profile/(?P<user_pk>\d+)/$', views.profile, name="profile"),
    url(r'^login/$', views.login_to_system, name="login"),
    url(r'^logout/$', views.logout_off_system, name="logout"),
    url(r'^get_notification/$', views.get_notification, name="get_notification"),
    url(r'^mark_all_as_read/$', views.mark_all_as_read, name="mark_all_as_read"),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)