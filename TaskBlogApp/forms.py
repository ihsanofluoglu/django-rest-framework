#!/usr/bin/env python
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from TaskBlogApp.models import Post, Comment, Category


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password', 'email', 'first_name', 'last_name'}


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'post_cat', 'post_content', 'post_title'}


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'comment_content'}


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = {'cat_title'}


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'post_content', 'post_title'}


class SearchForm(forms.Form):
    title = forms.CharField()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'email'}
