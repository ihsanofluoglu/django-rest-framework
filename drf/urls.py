from django.conf.urls import url, include
from rest_framework import routers

from drf import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet, base_name='category')
router.register(r'post', views.PostsViewSet, base_name='post')
router.register(r'comment', views.CommentViewSet, base_name='comment')
router.register(r'user', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^comment/(?P<id>[0-9]+)/like/$', views.CommentLikeViewSet.as_view({'get': 'get'}),
        name='comment-like'),
    url(r'^comment/(?P<id>[0-9]+)/dislike/$', views.CommentDislikeViewSet.as_view({'get': 'get'}),
        name='comment-dislike'),
    url(r'^post/(?P<id>[0-9]+)/like/$', views.PostLikeViewSet.as_view({'get': 'get'}),
        name='post-like'),
    url(r'^post/(?P<id>[0-9]+)/dislike/$', views.PostDislikeViewSet.as_view({'get': 'get'}),
        name='post-dislike'),

    url(r'^auth/', views.AuthViewSet.as_view({'post': 'post', 'delete': 'destroy'}), name='auth'),
]
