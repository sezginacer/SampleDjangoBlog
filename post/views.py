from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from models import Post

# Create your views here.

@login_required(login_url='/posts/login/')
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
        return HttpResponseRedirect('/posts/')
    return render(request, 'post/login.html')

def auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username = username, password = password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/posts/') # success
    else:
        return HttpResponseRedirect('/posts/login/') # error

def authh(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if (User.objects.filter(username__iexact=username).exists() or username == 'view' or
        username == 'delete' or username == 'edit'):
        return HttpResponseRedirect('/posts/register/') # error

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
    return HttpResponseRedirect('/posts/') # success

def logoutt(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/posts/login/')

@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/posts/')
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

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        #import ipdb; ipdb.set_trace()
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
        user = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(writer=user)
