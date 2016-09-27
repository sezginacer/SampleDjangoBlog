"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from django.views.generic import RedirectView
from post import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^posts/', include('post.urls')),
    # url(r'^$', RedirectView.as_view(url='/posts/')),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginn, name='login'),
    url(r'^register/$', views.signup, name='signup'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^authh/$', views.authh, name='authh'),
    url(r'^logout/$', views.logoutt, name='logout'),
    url(r'^api/$', views.PostListAPI.as_view(), name='api'),
    url(r'^view/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='postdetails'),
    url(r'^edit/(?P<pk>\d+)/$', views.PostUpdateView.as_view(), name='updatepost'),
    url(r'^new/$', login_required(views.PostCreateView.as_view(), login_url='/login/'), name='newpost'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(views.PostDeleteView.as_view(), login_url='/login/'), name='deletepost'),
    url(r'^profile/(?P<username>\w+)/$', views.UserPostsListView.as_view(), name='userpostslist'),
    url(r'^profile/(?P<username>\w+)/(?P<pk>\d+)/$', views.UserPostDetailView.as_view(), name='userpostsdetail'),
]
