"""TaskBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from TaskBlogApp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='post'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^sign_up/$', views.SignupView.as_view(), name='signup'),

    url(r'^add_post/$', views.AddPostView.as_view(), name='add_post'),
    url(r'^add_cat/$', views.AddCategoryView.as_view(), name='add_cat'),

    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/like_post/$', views.PlusLikePostView.as_view(),
        name='like_post'),
    url(r'^/category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/dislike_post/$', views.PlusDislikePostView.as_view(),
        name='dislike_post'),

    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/dislike_comment/(?P<comment_id>[0-9]+)/$',
        views.PlusDislikeCommentView.as_view(),
        name='dislike_comment'),
    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/like_comment/(?P<comment_id>[0-9]+)/$',
        views.PluslikeCommentView.as_view(),
        name='like_comment'),

    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/edit/$', views.EditPostView.as_view(),
        name='edit_post'),
    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/delete/$', views.DeletePostView.as_view(),
        name='delete_post'),

    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/comment/(?P<comment_id>[0-9]+)/edit/$',
        views.EditCommentView.as_view(),
        name='edit_comment'),
    url(r'^category/(?P<id>[0-9]+)/post/(?P<pk>[0-9]+)/comment/(?P<comment_id>[0-9]+)/delete/$',
        views.DeleteCommentView.as_view(),
        name='delete_comment'),

    url(r'^category/(?P<id>[0-9]+)/delete/$', views.DeleteCatView.as_view(), name='delete_cat'),
    url(r'^profile/(?P<id>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^profile/edit/(?P<id>[0-9]+)/$', views.EditProfileView.as_view(), name='edit-profile'),

    url(r'^api/', include('drf.urls', namespace='rest_framework')),
]
