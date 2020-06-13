from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.db import transaction
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from home.models import Profile
from multiphoto.forms import MultiForm, ImageFormSet, MultiCommentForm
from multiphoto.models import MultiPhoto, MultiComment


class MultiList(ListView):
    model = MultiPhoto
    paginate_by = 8

    def get_queryset(self):
        return MultiPhoto.objects.order_by('-created')


class MultiDetail(DetailView):
    model = MultiPhoto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multicomment_form'] = MultiCommentForm()
        return context


@login_required
def multi_create(request):
    if request.method == 'POST':
        multi_form = MultiForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if multi_form.is_valid() and image_formset.is_valid():
            post = multi_form.save(commit=False)
            post.author = request.user
            with transaction.atomic():
                post.save()
                image_formset.instance = post
                image_formset.save()
                return redirect('multiphoto:index')
    else:
        multi_form = MultiForm()
        image_formset = ImageFormSet()

    return render(request, 'multiphoto/multi_create.html', {
        'multi_form': multi_form,
        'image_formset': image_formset,
    })


@login_required
def multi_update(request, pk):
    post = get_object_or_404(MultiPhoto, pk=pk)
    if post.author != request.user:
        return redirect('multiphoto:index')
    else:
        if request.method == 'POST':
            multi_form = MultiForm(request.POST, instance=post)
            image_formset = ImageFormSet(request.POST, request.FILES, instance=post)
            if multi_form.is_valid() and image_formset.is_valid():
                multi_form.save()
                image_formset.save()

                return redirect('multiphoto:multi_detail', pk)
        else:
            multi_form = MultiForm(instance=post)
            image_formset = ImageFormSet(instance=post)
        return render(request, 'multiphoto/multi_create.html', {
            'multi_form': multi_form,
            'image_formset': image_formset,
        })


class MultiDelete(LoginRequiredMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = MultiPhoto

    success_url = '/multi'

    def get_object(self, queryset=None):
        post = super(MultiDelete, self).get_object()
        if post.author != self.request.user:
            raise PermissionError('Post 삭제 권한이 없습니다.')
        return post


class MyMultiList(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = MultiPhoto
    paginate_by = 8

    def get_queryset(self):
        object_list = MultiPhoto.objects.filter(author=self.request.user)
        return object_list.order_by('-created')


class MultiListByUser(ListView):
    paginate_by = 8

    def get_queryset(self):
        name = self.kwargs['username']
        user = User.objects.get(username=name)
        return user.multiphoto_set.order_by('-created')


def comment_create(request, pk):
    post = MultiPhoto.objects.get(pk=pk)
    form = MultiCommentForm(request.POST)
    if request.method == 'POST':
        current_user = request.user
        if current_user.is_authenticated:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        return render(request, 'home/login_require.html')
    else:
        return redirect(request, 'multicomment_form.html', {'form': form, })


class CommentUpdate(UpdateView):
    model = MultiComment
    form_class = MultiCommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


def comment_delete(request, pk):
    comment = MultiComment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url()+'#comment-list')
    else:
        return redirect('/multi')


class MyMultiCommentList(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = MultiComment
    paginate_by = 20

    def get_queryset(self):
        object_list = MultiComment.objects.filter(author=self.request.user)
        return object_list.order_by('-modified_at')


def multi_about(request):
    return render(request, 'multiphoto/about.html')