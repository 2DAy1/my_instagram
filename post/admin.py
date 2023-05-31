from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'full_name', 'bio', 'avatar', 'is_active', 'is_staff')
    list_display_links = ('id','username','email')
    search_fields = ('username', 'email', 'full_name', 'bio')
    list_filter = ('username', 'is_active', 'is_staff')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at','is_published')
    list_display_links = ('id', 'author')
    search_fields = ('author', 'caption')
    list_filter = ('is_published', 'created_at')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post','image')
    list_display_links = ('id', 'post','image')
    search_fields = ('post',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
