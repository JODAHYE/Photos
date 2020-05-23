from django.shortcuts import render

# Create your views here.
from unicodedata import category

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from home.forms import CommentForm
from home.models import Post, Category, Comment, Profile
from photo_site import settings


class PostList(ListView):
    model = Post
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['comment_form'] = CommentForm()
        return context


class PostListByCategory(ListView):
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        return category.post_set.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()

        return context


class PostListByUser(ListView):
    paginate_by = 8

    def get_queryset(self):
        name = self.kwargs['username']
        user = User.objects.get(username=name)
        return user.post_set.order_by('-created')


class PostUpdate(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Post
    fields = [
        'title', 'category', 'image', 'content'
    ]

    def get_object(self, queryset=None):
        post = super(PostUpdate, self).get_object()
        if post.author != self.request.user:
            return redirect('/')
        return post


class PostCreate(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Post
    fields = ['title', 'category', 'image', 'content']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/')


class PostDelete(LoginRequiredMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = Post

    success_url = '/'

    def get_object(self, queryset=None):
        post = super(PostDelete, self).get_object()
        if post.author != self.request.user:
            return redirect('/')
        return post


def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if request.user.is_anonymous:
        return render(request, 'home/login_require.html')

    profile = Profile.objects.get(user=request.user)
    check_like_post = profile.like_posts.filter(pk=pk)

    if check_like_post.exists():
        profile.like_posts.remove(post)
        post.like_count -= 1
        post.save()
    else:
        profile.like_posts.add(post)
        post.like_count += 1
        post.save()

    return redirect('home:post_detail', pk)


def comment_create(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        current_user = request.user
        if current_user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        return render(request, 'home/login_require.html')
    else:
        return redirect('/')


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            return redirect('/')
        return comment


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url()+'#comment-list')
    else:
        return redirect('/')


class MyPostList(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = Post
    paginate_by = 8

    def get_queryset(self):
        object_list = Post.objects.filter(author=self.request.user)
        return object_list.order_by('-created')


class MyCommentList(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = Comment
    paginate_by = 20

    def get_queryset(self):
        object_list = Comment.objects.filter(author=self.request.user)
        return object_list.order_by('-modified_at')


def about(request):
    return render(request, 'home/about.html')