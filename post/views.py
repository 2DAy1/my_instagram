from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView


from .forms import *
from .models import *
from .utils import *


# Create your views here.


class PostHome(LoginRequiredMixin,DataMixin, ListView):
    login_url = reverse_lazy('register')
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='My insta')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


def profile(request):
    return render(request, 'post/profile.html', context={'title': 'Profile'})


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'post/registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'post/registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')




def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect(reverse_lazy('login'))


def search_post(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'title': 'Found post',
        'tag_selected': 0,
    }
    return render(request, 'post/search_post.html', context=context)


class ShowPost(LoginRequiredMixin,DataMixin, DetailView):
    login_url = reverse_lazy('register')
    model = Post
    template_name = 'post/post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class CreatePost(DataMixin, CreateView):
    login_url = reverse_lazy('register')
    form_class = PostForm
    template_name = 'post/create_post.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Create post')
        return dict(list(context.items()) + list(c_def.items()))


class ShowTag(LoginRequiredMixin,DataMixin, ListView):
    login_url = reverse_lazy('register')
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['tag_slug']
        tag = get_object_or_404(Tag, slug=slug)
        c_def = self.get_user_context(title='Tag - ' + str(tag),
                                      tag_selected=self.kwargs['tag_slug'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.kwargs['tag_slug']
        tag = get_object_or_404(Tag, slug=slug)
        posts_list = tag.post_tags.values_list('post', flat=True)
        return Post.objects.filter(pk__in=posts_list, is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
