# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cat_title', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_content', models.CharField(max_length=100)),
                ('comment_like', models.IntegerField(default=0)),
                ('comment_dislike', models.IntegerField(default=0)),
                ('comment_createdAt', models.DateTimeField(auto_now_add=True)),
                ('comment_updatedAt', models.DateTimeField()),
                ('comment_author', models.ForeignKey(to='TaskBlogApp.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_title', models.CharField(max_length=70)),
                ('post_content', models.CharField(max_length=800)),
                ('post_createdAt', models.DateTimeField(auto_now_add=True)),
                ('post_updatedAd', models.DateTimeField()),
                ('post_like', models.IntegerField(default=0)),
                ('post_dislike', models.IntegerField(default=0)),
                ('post_author', models.ForeignKey(to='TaskBlogApp.Author')),
                ('post_cat', models.ForeignKey(to='TaskBlogApp.Category')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_post',
            field=models.ForeignKey(to='TaskBlogApp.Post'),
        ),
    ]
