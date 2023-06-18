from django import template

register = template.Library()

@register.filter
def user_has_liked(post, user):
    return post.likes.filter(id=user.id).exists()
