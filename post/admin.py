from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at','is_published')
    list_display_links = ('id', 'author')
    search_fields = ('author', 'caption')
    list_filter = ('is_published', 'created_at')


admin.site.register(Post, PostAdmin)
