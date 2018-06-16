from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
from django.utils.six import python_2_unicode_compatible
from TaskBlogApp.forms import LoginForm, SignupForm, AddPostForm, AddCommentForm, AddCategoryForm, UpdatePostForm, \
    SearchForm, EditProfileForm
from TaskBlogApp.models import Category, Post, Comment


class IndexView(generic.View):
    template_name = 'index.html'

    def get(self, request):
        try:
            categories = Category.objects.all()
            posts = Post.objects.order_by('-post_updatedAd')[:5]
        except Category.DoesNotExist:
            categories = None
            posts = None
        return render(request, 'index.html', {
            'categories': categories,
            'posts': posts})


class PostView(generic.View):
    template_name = 'post.html'

    def get(self, request, pk, id):
        comment_form = AddCommentForm()
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            post = None
        return render(request, 'post.html', {
            'post': post,
            'comment_form': comment_form,
            'comment_form_error': comment_form.errors})

    def post(self, request, pk, id):
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated():
                post = Post.objects.get(id=pk)

                comment_form.save(commit=False)
                comment_form.instance.comment_author = request.user
                comment_form.instance.comment_post = post
                comment_form.save()

                return HttpResponseRedirect('/category/%s/post/%s/' % (id, pk))
            else:
                return HttpResponseRedirect('/login/')
        else:
            try:
                post = Post.objects.get(id=pk)
            except Post.DoesNotExist:
                post = None
            return render(request, 'post.html', {
                'post': post,
                'comment_form': comment_form,
                'comment_form_error': comment_form.errors})


class CategoryView(generic.View):
    template_name = 'categories.html'

    def get(self, request, pk):
        try:
            posts = Post.objects.filter(post_cat_id=self.kwargs.get('pk')).order_by('post_updatedAd')
        except Post.DoesNotExist:
            posts = None
        return render(request, 'categories.html', {
            'posts': posts,
            'cat_pk': self.kwargs.get('pk')
        })


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            login_form = LoginForm()
            return render(request, 'login.html', {
                'login_form': login_form,
                'login_error': login_form.errors
            })
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        error = []
        login_form = LoginForm(request.POST)
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            if not password or not username:
                error = "Username or Password wrong!"

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {
                        'login_form': login_form,
                        'login_error': error
                    })
            else:
                error = "There is no such a user!"
                return render(request, 'login.html', {
                    'login_form': login_form,
                    'login_error': error
                })
        else:
            error = "Post Error"
            return render(request, 'login.html', {
                'login_form': login_form,
                'login_error': error
            })


class LogoutView(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')


class SignupView(generic.FormView):
    template_name = 'sign_up.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            sign_form = SignupForm()
            return render(request, 'sign_up.html', {
                'sign_form': sign_form,
                'sign_error': sign_form.errors})
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        sign_form = SignupForm(request.POST)
        if sign_form.is_valid():
            sign_form.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'sign_up.html', {
                'sign_form': sign_form,
                'sign_error': sign_form.errors})


class AddPostView(generic.FormView):
    template_name = 'add_post.html'
    form_class = AddPostForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            add_post_form = AddPostForm()
            return render(request, 'add_post.html', {
                'add_post_form': add_post_form,
                'post_error': add_post_form.errors})
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        add_post_form = AddPostForm(request.POST)
        if add_post_form.is_valid():
            add_post_form.save(commit=False)
            add_post_form.instance.post_author = request.user
            add_post_form.save()

            return HttpResponseRedirect('/')
        else:
            return render(request, 'add_post.html', {
                'add_post_form': add_post_form,
                'post_error': add_post_form.errors})


class AddCategoryView(generic.FormView):
    template_name = 'add_category.html'
    form_class = AddCategoryForm

    def get(self, request, *args, **kwargs):
        cat_form = AddCategoryForm()
        if request.user.is_authenticated():
            if request.user.is_superuser:

                return render(request, 'add_category.html', {
                    'cat_form': cat_form,
                    'cat_form_error': cat_form.errors
                })
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        cat_form = AddCategoryForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()

            return HttpResponseRedirect('/')
        else:
            return render(request, 'add_category.html', {
                'cat_form': cat_form,
                'cat_form_error': cat_form.errors
            })


class PlusLikePostView(generic.View):
    def get(self, request, pk, id):
        if request.user.is_authenticated():
            post = Post.objects.get(id=pk)
            post.post_like += 1
            post.save()

            return HttpResponseRedirect('/category/%s/post/%s/' % (id, pk))
        else:
            return HttpResponseRedirect('/login/')


class PlusDislikePostView(generic.View):
    def get(self, request, pk, id):
        if request.user.is_authenticated():
            post = Post.objects.get(id=pk)
            post.post_dislike += 1
            post.save()

            return HttpResponseRedirect('/category/%s/post/%s/' % (id, pk))
        else:
            return HttpResponseRedirect('/login/')


class PluslikeCommentView(generic.View):
    def get(self, request, pk, id, comment_id):
        if request.user.is_authenticated():
            comment = Comment.objects.get(id=comment_id)
            comment.comment_like += 1
            comment.save()

            return HttpResponseRedirect('/category/%s/post/%s' % (id, pk))
        else:
            return HttpResponseRedirect('/login/')


class PlusDislikeCommentView(generic.View):
    def get(self, request, pk, id, comment_id):
        if request.user.is_authenticated():
            comment = Comment.objects.get(id=comment_id)
            comment.comment_dislike += 1
            comment.save()

            return HttpResponseRedirect('/category/%s/post/%s' % (id, pk))
        else:
            return HttpResponseRedirect('/login/')


class EditPostView(generic.UpdateView):
    template_name = 'editPost.html'
    form_class = UpdatePostForm
    fields = ['post_content', 'post_title', 'post_updatedAd']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            post = Post.objects.get(id=kwargs['pk'])
            if request.user.pk == post.post_author_id or request.user.is_superuser:
                post_form = UpdatePostForm()
                return render(request, 'editPost.html', {
                    'post_form': post_form,
                    'post_form_error': post_form.errors
                })
            else:
                return HttpResponseRedirect('/category/%s/post/%s/' % (post.post_cat_id, kwargs['pk']))
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        post_form = UpdatePostForm(request.POST)
        if post_form.is_valid():
            post = Post.objects.get(id=kwargs['pk'])
            post.post_title = post_form.instance.post_title
            post.post_content = post_form.instance.post_content

            post.post_updatedAd = datetime.now()
            post.save()

            return HttpResponseRedirect('/category/%s/post/%s/' % (post.post_cat_id, kwargs['pk']))
        else:
            return render(request, 'editPost.html', {
                'post_form': post_form,
                'post_form_error': post_form.errors
            })


class DeletePostView(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            post = Post.objects.get(id=kwargs['pk'])
            if request.user.pk == post.post_author_id or request.user.is_superuser:
                post = Post.objects.get(id=kwargs['pk'])
                post.delete()

                return HttpResponseRedirect('/category/%s/' % kwargs['id'])
            else:
                return HttpResponseRedirect('/category/%s/' % kwargs['id'])

        else:
            return HttpResponseRedirect('/login/')


class EditCommentView(generic.FormView):
    template_name = 'editComment.html'
    form_class = AddCommentForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            comment = Comment.objects.get(id=kwargs['comment_id'])
            if request.user.pk == comment.comment_author_id or request.user.is_superuser:
                form = AddCommentForm()
                return render(request, 'editComment.html', {
                    'form': form,
                    'form_error': form.errors
                })
            else:
                return HttpResponseRedirect('/category/%s/post/%s/' % (kwargs['id'], kwargs['pk']))
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(id=kwargs['comment_id'])
            comment.comment_content = form.data.get('comment_content')
            comment.comment_updatedAt = datetime.now()
            comment.save()

            return HttpResponseRedirect('/category/%s/post/%s/' % (kwargs['id'], kwargs['pk']))

        else:
            return render(request, 'editComment.html', {
                'form': form,
                'form_error': form.errors
            })


class DeleteCommentView(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() or request.user.is_superuser:
            comment = Comment.objects.get(id=kwargs['comment_id'])
            if request.user.pk == comment.comment_author_id or request.user.is_superuser:
                comment = Comment.objects.get(id=kwargs['comment_id'])
                comment.delete()

                return HttpResponseRedirect('/category/%s/post/%s' % (kwargs['id'], kwargs['pk']))
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')


class DeleteCatView(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() or request.user.is_superuser:
            try:
                posts = Post.objects.filter(post_cat_id=self.kwargs.get('id'))
            except Category.DoesNotExist:
                posts = None
            try:
                cat_other = Category.objects.get(cat_title='other')
            except Category.DoesNotExist:
                cat_other = Category.objects.create(cat_title='other')

            if posts is not None:
                for post in posts:
                    post.post_cat = cat_other
                    post.save()

                cat_del = Category.objects.get(id=self.kwargs.get('id'))
                cat_del.delete()

                return HttpResponseRedirect('/category/%s/' % cat_other.id)
            else:
                return HttpResponseRedirect('/category/%s/' % self.kwargs.get('id'))

        else:
            return HttpResponseRedirect('/login/')


class ProfileView(generic.View):
    template_name = 'profile.html'

    def get(self, request, id):
        try:
            posts = Post.objects.filter(post_author=self.kwargs['id']).order_by('post_updatedAd')
        except Post.DoesNotExist:
            posts = None
        try:
            comments = Comment.objects.filter(comment_author=self.kwargs['id']).order_by('comment_updatedAt')
        except Comment.DoesNotExist:
            comments = None
        user = User.objects.get(pk=self.kwargs['id'])

        return render(request, 'profile.html', {
            'posts': posts,
            'comments': comments,
            'users': user,
            'id': int(self.kwargs.get('id'))
        })


class SearchView(generic.View):
    template_name = "search.html"

    def get(self, request):
        form = SearchForm()
        posts = None
        return render(request, 'search.html', {
            'form': form,
            'error': form.errors,
            'posts': posts
        })

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            posts = Post.objects.filter(post_title__icontains=form.data.get('title'))
            return render(request, 'search.html', {
                'form': form,
                'error': form.errors,
                'posts': posts
            })
        else:
            return render(request, 'search.html', {
                'form': form,
                'error': form.errors
            })


class EditProfileView(generic.View):
    template_name = 'edit-profile.html'

    def get(self, request, id):
        if request.user.pk == id:
            edit_form = EditProfileForm()
            return render(request, 'edit-profile.html', {
                'edit_form': edit_form,
                'edit_form_error': edit_form.errors
            })
        else:
            HttpResponseRedirect('/')

    def post(self, request, id):
        edit_form = EditProfileForm(request.POST)
        if edit_form.is_valid():
            users = User.objects.get(pk=id)
            users.username = edit_form.data.get('username')
            users.email = edit_form.data.get('email')
            users.save()
            return HttpResponseRedirect('/profile/%s' % id)
        else:
            return render(request, 'edit-profile.html', {
                'edit_form': edit_form,
                'edit_form_error': edit_form.errors
            })
