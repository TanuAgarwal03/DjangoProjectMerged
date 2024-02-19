from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from .forms import CustomUserCreationForm 
from .forms import CustomUserChangeForm
from .forms import PostForm
from .forms import CommentForm
from .models import Comment
from .models import Post
from .models import User

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(request ,request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:post_list')            
    else:
        form = AuthenticationForm()
    return render(request , 'blog/login.html', {'form' :form})

def logout_view(request):
    logout(request)
    return redirect('blog:post_list')  

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    print(posts)
    return render(request,'blog/post_list.html',{'posts' : posts})

def uploadok(request):
    return HttpResponse('upload successful')

def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    print("------")
    print(comments)
    print("------")
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            return redirect('blog:post_detail' , slug = slug)
    else:
        comment_form =CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post ,'new_comment' : new_comment ,'comments':comments , 'comment_form' : comment_form})

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

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:user_detail'  ,username=user.username) 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})

def user_detail(request, username):
    user = get_object_or_404(User,username=username)
    return render(request, 'blog/userdetails.html', {'user': user})

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

def index(request):
    return render(request, 'index.html')



    
