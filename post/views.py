from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .models import Post

# for REST API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer

import datetime

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    # return render(request, 'post/home.html')
    posts = Post.objects.filter(writer=request.user)
    '''
    c = {}
    c.update(posts=posts)
    c.update(username=request.user.username)
    '''
    '''
    c = {
        'posts':posts,
        'username':request.user.username
    }
    '''
    c = dict(posts=posts, username=request.user.username)
    return render(request, 'post/posts.html', c)


@csrf_protect
def loginn(request):
    # c = {}
    # c.update(csrf(request))
    # return render(request, 'post/login.html', c)
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'post/login.html')


def auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username = username, password = password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/') # success
    else:
        return HttpResponseRedirect('/login/') # error


def authh(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if (User.objects.filter(username__iexact=username).exists() or username == 'view' or
        username == 'delete' or username == 'edit' or username == 'login'):
        return HttpResponseRedirect('/register/')

    user = User.objects.create_user(username=username, password=password)
    '''
    user = User()
    user.username = username
    user.password = password
    user.save()
    '''
    '''
    user = User(username=username, password=password)
    user.save()
    '''
    login(request, user)
    return HttpResponseRedirect('/') # success


def logoutt(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/login/')


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return render(request, 'post/register.html')


class PostDetailView(DetailView):

    # import ipdb; ipdb.set_trace()

    model = Post

    def get_queryset(self):
        return Post.objects.filter(writer=self.request.user)

    '''
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context
    '''


class PostUpdateView(UpdateView):

    model = Post
    fields = ['title', 'text']
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        return reverse_lazy('postdetails', args=[self.object.id])

    def get_queryset(self):
        return Post.objects.filter(writer=self.request.user)


class PostCreateView(CreateView):

    model = Post
    fields = ['title', 'text']
    template_name_suffix = '_add_form'

    def get_success_url(self, **kwargs):
        return reverse_lazy('postdetails', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.writer = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostDeleteView(DeleteView):

     model = Post
     success_url = reverse_lazy('index')
     template_name_suffix = '_delete_form'

     def get_queryset(self):
         return Post.objects.filter(writer=self.request.user)


class UserPostsListView(ListView):

    model = Post
    template_name_suffix = '_user_list'
    # context_object_name = 'object_list' # default
    # paginate_by = 2

    def get_queryset(self):
        '''
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        '''
        user = get_object_or_404(User, username=self.kwargs['username'])
        # import ipdb; ipdb.set_trace()
        return Post.objects.filter(writer=user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserPostsListView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        return context


class UserPostDetailView(DetailView):

    model = Post
    template_name_suffix = '_user_detail'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        # return get_list_or_404(Post, writer=user) # returns list but must return queryset
        try:
            posts = Post.objects.filter(writer=user)
        except Post.DoesNotExist:
            raise Http404
        return posts


# Lists all posts or create new one
class PostListAPI(APIView):

    def get(self, request):
        if 'username' in request.GET:
            if User.objects.filter(username__iexact=request.GET.get('username')).exists():
                user = User.objects.filter(username__iexact=request.GET.get('username'))
                posts = Post.objects.filter(writer=user)
                serializer = PostSerializer(posts, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Error: No such user"}, status=status.HTTP_404_NOT_FOUND)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            if request.POST.get('title') is not None and request.POST.get('text') is not None:
                # writer = user
                title = request.POST.get('title')
                text = request.POST.get('text')
                # date = datetime.datetime.now()
                # post = Post(writer=user, title=title, text=text, date=date)
                # post.save()
                Post.objects.create(writer=user, title=title, text=text)
                return Response({"message": "Post added successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Error! Title and/or Text not provided!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message": "Error: Authentication Failed!"}, status=status.HTTP_401_UNAUTHORIZED)
