from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm
from posts.models import Post
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


# Create your views here.

@login_required(login_url='/login/')
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)

    if comment.user != request.user:
        # messages.success(request, "Successfully Deleted Comment")
        response= HttpResponse("You do not have permission to delete this comment")
        response.status_code= 403
        return response

    parent_object_url= comment.content_object.get_absolute_path()
    try:
        comment.delete()
    except:
        print("Something went wrong")
    messages.success(request, "Successfully Deleted Comment")
    return HttpResponseRedirect(parent_object_url)

def comment_thread(request, id):
    # obj= get_object_or_404(Comment, id=id)

    try:
        obj= Comment.objects.get(id=id)
        print(obj.is_parent())
    except:
        raise Http404

    if not obj.is_parent():
        obj= obj.parent

    initial_data = {
        'content_type': obj.content_type,
        'object_id': obj.object_id
    }

    form= CommentForm(request.POST or None, initial=initial_data)
    print(form.errors)
    if form.is_valid() and request.user.is_authenticated():
        content_type= ContentType.objects.get_for_model(Post)
        obj_id= form.cleaned_data.get("object_id")
        content_data= form.cleaned_data.get("content")
        parent_obj= None
        try:
            parent_id= int(request.POST.get("parent_id"))
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
        return HttpResponseRedirect(obj.get_absolute_path())

    return render(request, "comments/comment_thread.html", {"comment": obj, "form": form})