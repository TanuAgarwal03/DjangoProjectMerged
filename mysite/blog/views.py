from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.conf import settings
# from .models import Tag
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    print(posts)
    return render(request,'blog/post_list.html',{'posts' : posts})

def uploadok(request):
    return HttpResponse('upload successful')




def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        print(form.is_valid(),form)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', slug= post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST , instance=post) 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', slug= post.slug)
    else:
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form})

def list_posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {"category_name": category.name, "posts": posts}
    return render(request, "index.html", context)

def list_posts_by_tag( request , slug):
    tag = get_object_or_404(Tag,slug=slug)
    posts = Post.objects.filter(tags =tag)
    context ={'tag':tag,'posts' :posts,}
    return render(request , "home.html" ,context)
