from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm


# Create your views here.
def post_list(request):
    posts_list = Post.objects.active()
    if request.user.is_superuser or request.user.is_staff:
        posts_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(posts_list, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'posts/home.html', {'posts': posts})


def post_details(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if post.draft or post.date > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    return render(request, 'posts/post_details.html', {'post': post})


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_path())
    else:
        messages.error(request, "Something went wrong")

    context = {
        "form": form
    }
    return render(request, 'posts/post_form.html', context)


def post_delete(request, post_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=post_slug)
    post.delete()
    messages.success(request, "Successfully Deleted")
    return HttpResponseRedirect(reverse('posts:list'))


def post_update(request, post_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=post_slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_path())

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'posts/post_form.html', context)
