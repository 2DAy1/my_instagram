from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        user.is_active = False  # Set user as inactive until email confirmation
        user.save(using=self._db)

        # Send email confirmation
        self.send_email_confirmation(user)


        return user

    def send_email_confirmation(self, user):
        current_site = get_current_site(None)
        mail_subject = 'Confirm your email'
        message = render_to_string('registration/email_confirmation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@example.com', [user.email])

    def confirm_email(self, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = self.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return user

        return None

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, blank=False)
    full_name = models.CharField(max_length=255, blank=False)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_insta',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_insta',
        blank=True,
    )

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
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
        return reverse('post', kwargs={'post_pk': self.pk})


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=f'images/', blank=False)

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        self.image.upload_to = f'images/{self.post.author}'
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class PostTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='post_tags')

    def __str__(self):
        return f'Post: {self.post}, Tag:{self.tag}'


