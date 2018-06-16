from django.contrib import admin

# Register your models here.
from TaskBlogApp.models import Category, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_title')


class PostAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'post_cat', 'post_author', 'post_content', 'post_createdAt', 'post_updatedAd', 'post_like', 'post_dislike')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'comment_post', 'comment_author', 'comment_content', 'comment_like', 'comment_dislike',
        'comment_createdAt',
        'comment_updatedAt')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
