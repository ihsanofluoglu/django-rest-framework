#!/usr/bin/env python
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from TaskBlogApp.models import Category, Post, Comment
from drf.serializer import CategorySerializers, PostsSerializers, CommentSerializers, UserSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        global other
        if not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            other = Category.objects.get(cat_title='other')
        except Category.DoesNotExist:
            other = Category.objects.create(cat_title='other')

        posts = Post.objects.filter(post_cat_id=int(kwargs.get('pk')))

        for post in posts:
            post.post_cat = other
            post.save()

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if not request.user.is_superuser():
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.user.id != int(request.data.get('post_author')):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_superuser or request.user.id == instance.post_author_id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated() or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated() or request.user.is_superuser or request.user.id == int(
                request.data.get('comment_author')):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_superuser or request.user.id == instance.comment_author_id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def update(self, request, *args, **kwargs):
        if request.user.username == request.data.get(
                'username'):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentLikeViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def get(self, request, id=None):
        if id:
            comment = Comment.objects.get(id=id)
            comment.comment_like += 1
            comment.save()
            data = CommentSerializers(Comment.objects.get(pk=id)).data
            content = {'comment': data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not Modified."}, status=status.HTTP_304_NOT_MODIFIED)


class CommentDislikeViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def get(self, request, id=None):
        if id:
            comment = Comment.objects.get(id=id)
            comment.comment_dislike += 1
            comment.save()
            data = CommentSerializers(Comment.objects.get(pk=id)).data
            content = {'comment': data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not Modified."}, status=status.HTTP_304_NOT_MODIFIED)


class PostDislikeViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostsSerializers

    def get(self, request, id=None):
        if id:
            post = Post.objects.get(id=id)
            post.post_dislike += 1
            post.save()
            data = PostsSerializers(Post.objects.get(pk=id)).data
            content = {'post': data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not Modified."}, status=status.HTTP_304_NOT_MODIFIED)


class PostLikeViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostsSerializers

    def get(self, request, id=None):
        if id:
            post = Post.objects.get(id=id)
            post.post_like += 1
            post.save()
            data = PostsSerializers(Post.objects.get(pk=id)).data
            content = {'post': data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not Modified."}, status=status.HTTP_304_NOT_MODIFIED)


class AuthViewSet(viewsets.ViewSet):
    def get(self, request):
        return Response({'detail': "GET Response"})

    def post(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if not data.get('username') or not data.get('password'):
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.get(username=data.get('username'))
        if not user:
            return Response(
                'No default user, please create one',
                status=status.HTTP_404_NOT_FOUND
            )

        token = Token.objects.get_or_create(user=user)

        return Response({'detail': 'POST answer', 'token': token[0].key})

    def destroy(self, request):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.get(username=data.get('username')):
            token = Token.objects.get(user=User.objects.get(username=data.get('username')))
            token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)