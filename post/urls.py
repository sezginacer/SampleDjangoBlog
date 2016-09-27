from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginn, name='login'),
    url(r'^register/$', views.signup, name='signup'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^authh/$', views.authh, name='authh'),
    url(r'^logout/$', views.logoutt, name='logout'),
    url(r'^api/$', views.PostListAPI.as_view(), name='api'),
    url(r'^view/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='postdetails'),
    url(r'^edit/(?P<pk>\d+)/$', views.PostUpdateView.as_view(), name='updatepost'),
    url(r'^new/$', login_required(views.PostCreateView.as_view(), login_url='/posts/login/'), name='newpost'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(views.PostDeleteView.as_view(), login_url='/posts/login/'), name='deletepost'),
    url(r'^(?P<username>\w+)/$', views.UserPostsListView.as_view(), name='userpostslist'),
    url(r'^(?P<username>\w+)/(?P<pk>\d+)/$', views.UserPostDetailView.as_view(), name='userpostsdetail'),
]
