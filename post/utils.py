from django.db.models import Count
from django.http import JsonResponse
from django.core.cache import cache

from .models import *



class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        tags = cache.get('tags')

        if not tags:
            tags = Tag.objects.annotate(Count('post_tags'))
            cache.set('tags', tags, 60)

        context['tags'] = tags
        if 'tag_selected' not in context:
            context['tag_selected'] = 0



        return context



class LikePost:
    @staticmethod
    def like_post(request, post):
        if post.likes.filter(id=request.user.id).exists():
            # User has already liked the post, so remove the like
            post.likes.remove(request.user)
            liked = False
        else:
            # User hasn't liked the post, so add the like
            post.likes.add(request.user)
            liked = True

        # Return the updated like status and count
        response_data = {
            'liked': liked,
            'count': post.number_of_likes(),
        }
        return JsonResponse(response_data)
