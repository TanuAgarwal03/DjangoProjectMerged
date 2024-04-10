from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login , authenticate
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import *
from .models import *

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from gtts import gTTS

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:post_list')
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'blog/login.html', {"kk":"kk"})

def logout_view(request):
    logout(request)
    return redirect('blog:post_list')  

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts' : posts })

def uploadok(request):
    return HttpResponse('upload successful')

def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
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

def reply_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id') 
            mypost = Post.objects.filter(id=post_id).last()
            parent_id = request.POST.get('parent')  
            post_url = request.POST.get('post_url')
            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect('blog:post_detail' , slug = mypost.slug)
    return redirect("/")

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
    return render(request, 'blog/post_edit.html', {'form': form,'page':'New'})
    
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST , instance=post) 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', slug= post.slug)
    else:
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form,'page':'Edit'})

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


def cat_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/cat_list.html', {'categories':categories})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags':tags})

def cat_details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(category=categories)
    category_slug = "Category for: "+category_slug
    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories,"query":category_slug})

def tag_details(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)
    posts = Post.objects.filter(tags=tag)
    tag_title = "Tag for: " + tag_title
    return render(request, 'blog/post_list.html', {'posts': posts, 'tag': tag, 'query': tag_title})
    
def index(request):
    return render(request, 'polls/index.html')


# def generate_speech_view(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     audio_file_path = post.generate_speech()
#     return render(request, 'generate_speech.html', {'audio_file_path': audio_file_path})

# def home(request):
#     signals.notification.send(sender=None,request= request,user=['Geeky' , 'shows'])
#     return HttpResponse("this is the home page")

# def handle_post_text_changed(sender , instance, **kwargs):
#     print("Changes in text field")

# @csrf_exempt
# def handle_post_text_change_view(request):
#     # This view can handle incoming signals or serve as a placeholder
#     return HttpResponse("Signal received and processed")

