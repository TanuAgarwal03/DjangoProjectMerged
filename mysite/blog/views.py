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
from django.urls import reverse


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
    print("-------------")
    print(Post.tag)
    print("-------------")

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


def reply_comment(request):
    # post = get_object_or_404(Post, slug=slug)
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
            # return redirect(post_url+'/#'+str(reply.id))
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
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST , instance=post) 
        if form.is_valid():
            post = form.save(commit=False)
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

def index(request):
    return render(request, 'index.html')

def cat_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/cat_list.html', {'categories':categories})

def tag_list(request):
    tag = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tag':tag})

def cat_details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(category=categories)
    category_slug = "Category for: "+category_slug
    return render(request, 'blog/post_list.html', {'posts': posts,'categories':categories,"query":category_slug})

def tag_details(request, tag_slug):
    tag = get_object_or_404(Tag, name=tag_slug)
    posts = Post.objects.filter(tag=tag)
    tag_slug = "Tag for: "+tag_slug
    return render(request, 'blog/post_list.html', {'posts': posts,"query":tag_slug})

# def export_query_to_csv(request):
#     data = User.objects.all()
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="user.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['dob','image' , 'gender' ,'state','country']) 
#     user_fields = data.values_list('dob','image' , 'gender' ,'state','country')
#     for user in data:
#         writer.writerow([])
#     return response
