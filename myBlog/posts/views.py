from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
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

    initial_data= {
        'content_type': post.get_content_type,
        'object_id': post.id
    }

    comment_form= CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated():
        content_type= ContentType.objects.get_for_model(post)
        print(content_type)
        obj_id= comment_form.cleaned_data.get("object_id")
        print(obj_id)
        content_data= comment_form.cleaned_data.get("content")
        print(content_data)
        parent_obj= None
        try:
            parent_id= int(request.POST.get("parent_id"))
            print(parent_id)
        except:
            parent_id= None

        if parent_id:
            parent_qs= Comment.objects.filter(id=parent_id)
            if parent_qs and parent_qs.count()==1:
                parent_obj=parent_qs.first()

        new_comment, created= Comment.objects.get_or_create(
            user= request.user,
            content_type= content_type,
            object_id=obj_id,
            parent=parent_obj,
            content= content_data
        )

        print(new_comment)
        return HttpResponseRedirect(post.get_absolute_path())

    return render(request, 'posts/post_details.html', {'post': post,'comment_form': comment_form})

@login_required(login_url='/login/')
def post_create(request):
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

@login_required(login_url='/login/')
def post_delete(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if not request.user == post.user:
        response = HttpResponse("You do not have permission to delete this post")
        response.status_code = 403
        return response
    post.delete()
    messages.success(request, "Successfully Deleted")
    return HttpResponseRedirect(reverse('posts:list'))

@login_required(login_url='/login/')
def post_update(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if not request.user == post.user:
        response = HttpResponse("You do not have permission to update this post")
        response.status_code = 403
        return response
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
