from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from TaskBlogApp.models import Category, Post, Comment


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
