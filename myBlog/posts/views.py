from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts_list= Post.objects.all()
    paginator = Paginator(posts_list, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request,'posts/home.html',{'posts':posts})

def post_details(request, post_slug):
    post= get_object_or_404(Post, slug=post_slug)
    return render(request, 'posts/post_details.html', {'post':post})

def post_create(request):
    form= PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance= form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_path())
    else:
        messages.error(request, "Something went wrong")

    context={
        "form": form
    }
    return render(request, 'posts/post_form.html', context)

def post_delete(request, post_slug):
    post= get_object_or_404(Post, slug=post_slug)
    post.delete()
    messages.success(request,"Successfully Deleted")
    return HttpResponseRedirect(reverse('posts:list'))

def post_update(request, post_slug):
    post= get_object_or_404(Post, slug=post_slug)
    form = PostForm(request.POST or None,  request.FILES or None ,instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_path())

    context={
        'post': post,
        'form':form
    }
    return render(request, 'posts/post_form.html', context)
