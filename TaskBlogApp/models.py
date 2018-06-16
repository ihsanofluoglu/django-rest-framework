from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Category(models.Model):
    cat_title = models.CharField(max_length=70)

    def __str__(self):
        return self.cat_title

@python_2_unicode_compatible
class Post(models.Model):
    post_cat = models.ForeignKey(Category)
    post_author = models.ForeignKey(User)

    post_title = models.CharField(max_length=70)
    post_content = models.TextField()

    post_createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post_updatedAd = models.DateTimeField(auto_now_add=False, default=datetime.now)

    post_like = models.IntegerField(default=0)
    post_dislike = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title


@python_2_unicode_compatible
class Comment(models.Model):
    comment_post = models.ForeignKey(Post)
    comment_author = models.ForeignKey(User)

    comment_content = models.CharField(max_length=100)
    comment_like = models.IntegerField(default=0)
    comment_dislike = models.IntegerField(default=0)

    comment_createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    comment_updatedAt = models.DateTimeField(auto_now_add=False, default=datetime.now)

    def __str__(self):
        return self.comment_content
