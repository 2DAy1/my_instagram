# Generated by Django 4.2.1 on 2023-05-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_remove_post_cat_delete_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at', 'author'], 'verbose_name': "User's posts", 'verbose_name_plural': "User's posts"},
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='post/'),
        ),
    ]
