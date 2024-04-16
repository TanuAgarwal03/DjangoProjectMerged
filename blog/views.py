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

from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib import messages
from django.utils.text import slugify
from django.db import IntegrityError
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

            for index, row in df.iterrows():

                try:
                    # user_fk_instance = User.objects.filter(username=row['user_fk']).last()
                    # if not user_fk_instance:
                    #     user_fk_instance = User.objects.create(username=row['user_fk'])

                    # user_oto_instance = User.objects.filter(username=row['user_oto']).last()
                    # if not user_oto_instance:
                    #     # If user_oto does not exist, raise an exception to handle it later
                    #     raise Exception(f"User with username '{row['user_oto']}' does not exist")


                    user_fk_instance, created_fk = User.objects.get_or_create(username=row['user_fk'])
                    user_oto_instance, created_oto = User.objects.get_or_create(username=row['user_oto'])
                    if Testing.objects.filter(user_oto=user_oto_instance).exists():
                        raise Exception(f"Testing instance with user_oto '{row['user_oto']}' already exists")

                    # try:
                    #     user_oto_instance = User.objects.get(username=row['user_oto'])
                    # except User.DoesNotExist:
                    #     user_oto_instance = User.objects.create(username=row['user_oto'])
                    # # user_oto_instance, created_oto = User.objects.get_or_create(username=row['user_oto'])

                    slug = slugify(row['name'])
                    counter = 1
                    while Testing.objects.filter(slug=slug).exists():
                        slug = f"{slug}-{counter}"
                        counter += 1

                    date_value = row['date']
                    time_value = row['time']
                    if pd.notnull(date_value) and pd.notnull(time_value):
                        date_time = make_aware(datetime.combine(date_value, time_value))
                    else:
                        date_time = None

                
                    # user_id = row['user_oto']
                    # if Testing.objects.filter(user_oto_id = user_id).exists():
                    #     print(f"Skipping row {index + 1}: User ID '{user_id}' already exists.")
                    # else:
                    testing_instance = Testing.objects.create(
                        user_fk=user_fk_instance,
                        user_oto=user_oto_instance,
                        name=row['name'],
                        slug=slug,
                        image=row['image'],
                        file=row['file'],
                        about=row['about'],
                        date=row['date'],
                        time=row['time'],
                        published=row['published'],
                        email=row['email'],
                        url=row['url'],
                        pin=row['pin'],
                        verify=row['verify'],
                        state=row['state'],
                        country=row['country'],
                        latitude=row['latitude'],
                        longitude=row['longitude'],
                        # user_oto_id = user_id
                    )
                except IntegrityError as e:
                    messages.warning(request, f"Skipping row {index+1}: {str(e)}")
                    continue  # Move to the next row
                except Exception as e:
                    messages.error(request, f"Error occurred while saving data for row {index+1}: {str(e)}")
                    continue  # Move to the next row
            
            print("Success")

            messages.success(request, "Data uploaded successfully!")
            
            return redirect('blog:post_list')
        
    else:
        form = BulkPostUploadForm()
    testing_instances = Testing.objects.all()
    return render(request , 'blog/bulk_post_upload.html' , {'form' : form,'testing_instances': testing_instances})




  
        
        # for testing_instance in testing_instances:

            # for _, row in df.iterrows():
            #     try:
            #         slug = slugify(row['name'])
            #         user_fk_instance, created_fk = User.objects.get_or_create(username=row['user_fk'])
            #         user_oto_instance, created_oto = User.objects.get_or_create(username=row['user_oto'])

            #         testing_instance = Testing.objects.create(
            #             user_fk=user_fk_instance,
            #             user_oto=user_oto_instance,
            #             name=row['name'],
            #             slug=slug,
            #             image=row['image'],
            #             file=row['file'],
            #             about=row['about'],
            #             date=row['date'],
            #             time=row['time'],
            #             published=row['published'],
            #             email=row['email'],
            #             url=row['url'],
            #             pin=row['pin'],
            #             verify=row['verify'],
            #             state=row['state'],
            #             country=row['country'],
            #             latitude=row['latitude'],
            #             longitude=row['longitude']
            #         )

            #     except IntegrityError as e:
            #         print(f"IntegrityError: {e}")

            # # return redirect('blog:post_list')

            # return render(request, "blog/excel_to_html.html")


# 2012-09-04 06:00:00.000000-08:00