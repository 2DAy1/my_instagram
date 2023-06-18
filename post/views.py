from captcha.models import CaptchaStore
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, JsonResponse
from captcha import helpers
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *


# Create your views here.




class ShowPost(LoginRequiredMixin, DataMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'post/show_post.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        context = self.get_context_data(post=post)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        return LikePost.like_post(request, post)

    def get_object(self):
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        return post

    def get_context_data(self, **kwargs):
        context = {}
        post = kwargs.get('post')
        if post:
            context['post'] = post
            context['number_of_likes'] = post.number_of_likes()
            context['post_is_liked'] = post.likes.filter(id=self.request.user.id).exists()

        c_def = self.get_user_context(title=context.get('post'))
        context.update(c_def)
        return context

class PostHome(LoginRequiredMixin, DataMixin, ListView):
    login_url = reverse_lazy('login')
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='My insta')
        context.update(c_def)
        return context

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True).select_related('author').prefetch_related(
            Prefetch('post_tags', queryset=PostTag.objects.select_related('tag')),
            Prefetch('images')
        )
        return queryset

    def post(self, request, *args, **kwargs):
        post_pk = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_pk)
        return LikePost.like_post(request, post)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')

        captcha_id = CaptchaStore.generate_key()
        captcha_image_url = helpers.captcha_image_url(captcha_id)

        return {**context, **c_def, 'captcha_image_url': captcha_image_url, 'captcha_id': captcha_id}

    def form_invalid(self, form):
        # Increment the login attempts count
        if 'login_attempts' not in self.request.session:
            self.request.session['login_attempts'] = 1
        else:
            self.request.session['login_attempts'] += 1

        # If login attempts reach 2, add captcha field to form
        if self.request.session.get('login_attempts', 0) >= 2:
            form.fields['captcha'] = CaptchaField()

        return super().form_invalid(form)

    def get_response_error(self, form):
        # Customize the response when captcha validation fails
        # You can modify this method to handle the failure scenario as per your requirements
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Reset the login attempts count
        self.request.session['login_attempts'] = 0

        return super().form_valid(form)

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









class CreatePost(DataMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = PostForm
    template_name = 'post/create_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Create post')
        return dict(list(context.items()) + list(c_def.items()))


class ShowTag(LoginRequiredMixin, DataMixin, ListView):
    login_url = reverse_lazy('login')
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_tag()
        c_def = self.get_user_context(title='Tag - ' + str(tag.name),
                                      tag_selected=tag.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        tag = self.get_tag()
        queryset = Post.objects.filter(
            post_tags__tag=tag, is_published=True
        ).select_related('author').prefetch_related(
            Prefetch('post_tags', queryset=PostTag.objects.select_related('tag')),
            Prefetch('images')
        )
        return queryset

    def get_tag(self):
        slug = self.kwargs['tag_slug']
        cache_key = f'tag_{slug}'
        tag = cache.get(cache_key)
        if tag is None:
            tag = get_object_or_404(Tag, slug=slug)
            cache.set(cache_key, tag)
        return tag

def liked_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
