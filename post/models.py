from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User\'s posts'
        verbose_name_plural = 'User\'s posts'
        ordering = ['-created_at', 'author']

    def __str__(self):
        return f'{self.pk}) {self.author}: {self.caption[:10]}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='post/')

    def __str__(self):
        return self.image_url


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_id': self.pk})


class PostTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='post_tags')

    def __str__(self):
        return f'Post: {self.post}, Tag:{self.tag}'


