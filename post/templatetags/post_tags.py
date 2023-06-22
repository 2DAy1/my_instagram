from django import template
from post.models import *

register = template.Library()

menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'Search', 'url_name': 'search_post'},
    {'title': 'Create', 'url_name': 'create_post'},
]


@register.simple_tag(name='menu')
def get_menu():
    return menu


@register.inclusion_tag('post/tags/list_menu.html', takes_context=True)
def show_menu(context):
    return {'menu': menu, 'user': context.request.user}

@register.inclusion_tag('post/tags/post.html')
def show_post(post):
    return {'post': post}
