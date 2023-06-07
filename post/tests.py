from django.test import TestCase

# Create your tests here.

def create_test_data():
    from django.utils.crypto import get_random_string
    from faker import Faker
    from post.models import User, Post, Image, Tag, PostTag

    # Create a Faker instance
    fake = Faker()

    # Create 3 users
    users = []
    for i in range(2):
        user = User.objects.create(
            email=f'user{i + 1}@example.com',
            username=f'user{i + 1}',
            full_name=f'User {i + 1}',
            bio=f'Bio for User {i + 1}',
            avatar=f'avatars/avatar{i + 1}.jpg'
        )
        users.append(user)

    User.objects.bulk_create(users)

    # Create posts for each user
    posts = []
    for user in users:
        posts.extend([
            Post(author=user, caption=fake.paragraph(nb_sentences=fake.random_int(min=100, max=400)))
            for _ in range(2)
        ])

    Post.objects.bulk_create(posts)

    # Create images for each post
    images = []
    for post in Post.objects.all():
        num_images = Post.objects.filter(author=post.author).count() % 3 + 1
        images.extend([
            Image(post=post, image=f'images/image{post.pk}_{i + 1}.jpg')
            for i in range(num_images)
        ])
        for image in images:
            image.save()

    Image.objects.bulk_create(images)

    # Create tags
    tags = [Tag.objects.get_or_create(name=f'tag{i + 1}', slug=f'tag-{i + 1}')[0] for i in range(2)]

    # Associate tags with posts
    post_tags = []
    for post in Post.objects.all():
        post_tags.extend([
            PostTag(post=post, tag=tag)
            for tag in tags
        ])

    PostTag.objects.bulk_create(post_tags)


