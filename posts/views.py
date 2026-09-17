# from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic import ListView

#def post_list(request):
    #posts = Post.objects.all()
    #return render(request, "post_list.html", {"posts": posts})

class PostList(ListView): # new
    model = Post
    template_name = "post_list.html"