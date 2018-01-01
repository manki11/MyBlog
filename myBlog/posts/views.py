from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts= Post.objects.order_by('date')
    return render(request,'posts/home.html',{'posts':posts})

def post_details(request, post_id):
    post= get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_details.html', {'post':post})

def post_create(request):
    form= PostForm(request.POST or None)
    if form.is_valid():
        instance= form.save(commit=False)
        instance.save()

    context={
        "form": form
    }
    return render(request, 'posts/post_create.html', context)

def post_delete(request, post_id):
    post= get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_details.html', {'post':post})

def post_update(request, post_id):
    post= get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_details.html', {'post':post})
