from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .forms import *
from .models import *


# Create your views here.
menu = [
    {'title': 'Home', 'url_name': 'index'},
    {'title': 'Search', 'url_name': 'search_post'},
    {'title': 'Create', 'url_name': 'create_post'},
    {'title': 'Profile', 'url_name': 'user_cabinet'},
]


def index(request):
    posts = Post.objects.all()


    context = {
        'posts': posts,
        'title': 'Home',
        'tag_selected': 0,
    }
    return render(request, 'post/index.html', context=context)


def user_cabinet(request):
    return render(request, 'post/user_cabinet.html', context={'title': 'My Cabinet'})


def register(request): ...


def login(request): ...


def search_post(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'title': 'Found post',
        'tag_selected': 0,
    }
    return render(request, 'post/search_post.html', context=context)


def show_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
        'author': post.author,
    }
    return render(request, 'post/post.html', context=context)


def create_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddPostForm()
    context = {
        'from':form,
        'title': 'Create post'
    }

    return render(request, 'post/create_post.html',context=context)


def show_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts_list = tag.post_tags.values_list('post', flat=True)
    posts = Post.objects.filter(pk__in=posts_list)
    tags = Tag.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'tags': tags,
        'title': 'Posts by tags',
        'tag_selected': tag_id,
    }
    return render(request, 'post/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
