from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(60)(PostHome.as_view()), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('posts/', search_post, name='search_post'),
    path('posts/<int:post_pk>/', ShowPost.as_view(), name='post'),
    path('create', CreatePost.as_view(), name='create_post'),
    path('profile', profile, name='profile'),
    path('tag/<slug:tag_slug>/', ShowTag.as_view(), name='tag')
]