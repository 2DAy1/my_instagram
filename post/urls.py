from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('posts/', search_post, name='search_post'),
    path('posts/<int:post_id>/', show_post, name='post'),
    path('create', create_post, name='create_post'),
    path('my_cabinet', user_cabinet, name='user_cabinet'),
    path('tag/<int:tag_id>/', show_tag, name='tag')
]