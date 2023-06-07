from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class DataMixin:


    def get_user_context(self, **kwargs):
        context = kwargs
        context['tags'] = Tag.objects.all()
        if 'tag_selected' not in context:
            context['tag_selected'] = 0

        return context