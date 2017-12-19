from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):

    posts= Post.objects.order_by('date')

    return render(request,'posts/home.html',{'posts':posts})
