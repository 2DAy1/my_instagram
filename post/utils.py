from django.db.models import Count

from .models import *
from django.core.cache import cache



class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        tags = cache.get('tags')

        if not tags:
            tags = Tag.objects.annotate(Count('post_tags'))
            cache.set('tags', tags, 60)

        context['tags'] =tags
        if 'tag_selected' not in context:
            context['tag_selected'] = 0

        return context