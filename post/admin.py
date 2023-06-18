from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'full_name', 'bio', 'avatar', 'is_active', 'is_staff')
    list_display_links = ('id','username','email')
    search_fields = ('username', 'email', 'full_name', 'bio')
    list_filter = ('username', 'is_active', 'is_staff')



class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'get_html_images', 'is_published')
    list_display_links = ('id', 'author')
    list_editable = ('is_published',)
    search_fields = ('author', 'caption')
    list_filter = ('is_published', 'created_at')
    fields = ( 'author','caption', 'created_at','get_html_images', 'update_at')
    readonly_fields = ('author','created_at', 'update_at', 'get_html_images')

    def get_html_images(self, obj):
        images_html = ''
        if obj.images.all():
            for image in obj.images.all():
                images_html += f'<img src="{image.image.url}" width="50" />&nbsp;'
        return mark_safe(images_html)

    get_html_images.short_description = 'Images'





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

admin.site.site_title = 'MyInsta'
admin.site.site_header = 'Admin site | MyInsta'
