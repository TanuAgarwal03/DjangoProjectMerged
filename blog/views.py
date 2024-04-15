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

import pandas as pd

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
    # m = User.objects.get(username=request.POST["username"])
    # if request.method == "POST":
    #     if request.session.test_cookie_worked():
    #         request.session.delete_test_cookie()
    #         return HttpResponse("You're logged in.")
    #     else:
    #         return HttpResponse("Please enable cookies and try again.")
    # request.session.set_test_cookie()
    # return render(request, "blog/login.html")


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
#implementing sessions for storing username and password
        if user is not None: 
            request.session['username'] = username
            request.session['password'] = password
            print(request.session.get('username'))
            print(request.session.get('password'))
        if user is not None:
            login(request, user)
            return redirect('blog:post_list')
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'blog/login.html', {"kk":"kk"})

user_logout_signal = Signal()

def logout_view(request):
    # print("user logged out")
    # if request.user.is_authenticated:
    #     user_logout_signal.send(sender=request , user= request.user)
    logout(request)
    return redirect('blog:post_list')  



# def custom_logout_view(request):
#     print(f"User logged out.")
#     if request.user.is_authenticated:
#         user_logout_signal.send(sender=request, user=request.user)
#         logout(request)
#     return redirect('blog/login.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    #implementing sessions for last created post
    last_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-created_date').first()
    
    # Store the ID or title of the last post in the session
    # if last_post is not None:
    #     request.session['last_post_id'] = last_post.id
    #     request.session['last_post_title'] = last_post.title
    #     print(request.session.get('last_post_ids'))
    #     print(request.session.get('last_post_title'))
    
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

def test_add(request):
    print("Accessed test_add")
    if request.method == 'POST':
        form = TestingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
    else:
        form = TestingForm()
    return render(request, 'blog/test_add.html', {'form': form})

def bulk_post_upload(request):
    if request.method == 'POST':

        form = BulkPostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file= request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            # print(excel_file)

            # print(single_row)
            # for row in list1:
            #     for entry in row:
            #         print(entry)

            html_filename = "blog/templates/blog/excel_to_html.html"
            # html_content = df.to_html(index=False, classes='table', header='true', border=1, justify='left')
            html_content = '<table border="1">\n'
            html_content += '<thead>\n<tr>\n'
            for column in df.columns:
                html_content += f'<th>{column}</th>\n'
            html_content += '</tr>\n</thead>\n'
            
            html_content += '<tbody>\n'
            for i, row in enumerate(df.itertuples(), start=1):
                html_content += f'<tr id="row_{i}" name="row_{i}">\n'
                for value in row[1:]:  # Exclude the index
                    html_content += f'<td>{value}</td>\n'
                html_content += '</tr>\n'
            html_content += '</tbody>\n'
            html_content += '</table>\n'
            html_content += '<input type="submit" value="Submit" class = "btn btn-primary">'
            html_content = f'<form method="post" enctype="multipart/form-data">{html_content}</form>'
            
            with open(html_filename, 'w') as f:
                f.write(html_content)
            
            

            # for _, row in df.iterrows():
            #     instance = BulkPostUploadForm(excel_file=row['column1'])  
            #     instance.save()

            # form.save()
            return render(request, "blog/excel_to_html.html")
    else:
        form = BulkPostUploadForm()
    return render(request , 'blog/bulk_post_upload.html' , {'form' : form})












        # fields =request.FILES.getlist('excel_files')
        # for field in fields:
        #     field_ins = BulkPostUploadForm(excel_file = field)
        #     field_ins.save()
        # return redirect('blog:post_list')








# def bulk_post_upload(request):
#     if request.method == 'POST':
#         form = BulkPostUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']
#             df = pd.read_excel(excel_file)
#             html_content = df.to_html(index=False, classes='table', header='true', border=1, justify='left')
#             # Enclose HTML content in a form element
#             html_content = f'<form method="post" enctype="multipart/form-data">{html_content}</form>'
#             return render(request, "blog/excel_to_html.html", {'html_content': html_content})
#     else:
#         form = BulkPostUploadForm()
#         html_content = None
#     return render(request , 'blog/bulk_post_upload.html' , {'form' : form, 'html_content': html_content})

# def bulk_post_upload(request):
#     if request.method == 'POST':
#         form = BulkPostUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']
#             df = pd.read_excel(excel_file)
#             html_content = df.to_html(index=False, classes='table', header='true', border=1, justify='left')
#             return render(request, "blog/bulk_post_upload.html", {'form': form, 'html_content': html_content})
#     else:
#         form = BulkPostUploadForm()
#         html_content = None
#     return render(request , 'blog/bulk_post_upload.html' , {'form' : form, 'html_content': html_content})

#             columns = df.columns.tolist()
#             list1 = df.values.tolist()
#             # print(list1)
#  # Change this to the index of the row you want to access
#             single_row = list1[1]

#            
# for _, row in df.iterrows():
#                 tag_names = [tag.strip() for tag in row['tags'].split(',')]
#                 tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tag_names]
#                 category_name = row['category']
#                 category, created = Category.objects.get_or_create(title=category_name)
#                 post = Post.objects.create(
#                     title=row['title'],
#                     text=row['text'],
#                     author=request.user,
#                     published_date=row['published_date'],
#                     image=row['image'],
#                     feature_img= row['feature_img'],
#                     post_cat=category
#                 )
#                 post.tags.add(*tags)
# def save_data(request):
#     if request.method == 'POST':
#         # Process and save the data to the database
#         excel_file = request.FILES['excel_file']
#         df = pd.read_excel(excel_file)

#         # Iterate over the DataFrame rows
#         for _, row in df.iterrows():
#             # Create an instance of YourModelName and populate it with data from the DataFrame
#             instance = TestingForm()
#             # Save the instance to the database
#             instance.save()

#         return redirect('blog:post_list')
#     else:
#         return HttpResponse("Method Not Allowed", status=405)

