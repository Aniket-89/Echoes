from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.db.models import Q
from .models import Post, Author
from .forms import PostForm, RawPostForm
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# from django.urls import reverse


def home_view(request, *args, **kwargs):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(title__icontains=q) |
        Q(summary__icontains=q)
    )
    post_count = Post.objects.count()
    

    context = {'posts':posts, 'post_count': post_count}
    return render(request, 'blog/home.html', context)



def post_view(request, pk):
    post = Post.objects.get(id=pk)
    author = post.author

    context ={'post':post, 'author':author}
    return render(request, 'blog/post.html', context)


def author_view(request, pk):
    author = Author.objects.get(id=pk)
    context = {'author':author}
    return render(request, 'blog/author.html', context)


@login_required(login_url='login')
def edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = RawPostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post.title   = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.summary = form.cleaned_data['summary']
            new_image   = request.FILES.get('image')
            
            if new_image:
                # Resize the new image before saving
                resized_image = resize_image(new_image)
                post.image.delete()  # Delete the existing image file
                post.image = resized_image


            post.save()
            
            return redirect('post', pk)

    else:
        form = RawPostForm(initial={'title': post.title, 'content': post.content, 'summary': post.summary, 'image':post.image})

    context = {'form': form, 'post': post}
    return render(request, 'blog/edit.html', context)



def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')

    else:
        form = UserCreationForm()

    context = {'form':form}
    return render(request, 'blog/register.html', context)


def login_view(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
         
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'blog/login.html', {'error_message': error_message})
        
    return render(request, 'blog/login.html', {})


# @login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')


def about_view(request):
    return render(request, 'blog/about.html', {})


@login_required(login_url='login')
def delete_view(request, pk):
    obj = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('../../')
    
    context = {'post': obj}
    return render(request, 'blog/delete.html', context)


@login_required(login_url='login')
def create_view(request):
    form    = RawPostForm()
    if not hasattr(request.user, 'author'):
        # Create an Author object for the user if it doesn't exist
        author = Author.objects.create(user=request.user)
    else:
        author = request.user.author

    if request.method == 'POST':
        form = RawPostForm(request.POST, request.FILES)

        if form.is_valid():
            title   = form.cleaned_data['title']
            content = form.cleaned_data['content']
            summary = form.cleaned_data['summary']
            image   = request.FILES.get('image')

            if image:
                resized_image = resize_image(image)
                image = resized_image

            post = Post.objects.create(
                title   = title,
                content = content,
                summary = summary,
                author  = author,
                image   = image
            )
            return redirect('post', pk=post.id)
    
    context = {'form':form}
    return render(request, 'blog/create.html', context)

def resize_image(image):
    img = Image.open(image)
    max_width = 800
    max_height = 600
    img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    image_buffer = BytesIO()
    img.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    resized_image = InMemoryUploadedFile(
        image_buffer,
        None,  # Field name
        'resized.jpg',  # File name
        'image/jpeg',  # Content type
        img.tell,  # Size function
        None  # Content type extra headers
    )
    return resized_image

# Raw HTML form
# def create_view(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')        
#         content = request.POST.get('content')
#         summary = request.POST.get('summary')
        
#         author, created = Author.objects.get_or_create(user=request.user)

#         post = Post.objects.create(
#             title = title,
#             author = author,
#             content = content,
#             summary = summary,
#         )
#         return redirect('post', pk=post.pk)
#     context = {}
#     return render(request, 'blog/create.html', context)


# Using modelFOrms
# def create_view(request):
#     form = PostForm()

#     if request.method == 'POST':
#         form = PostForm(request.POST)
    
#         if form.is_valid():
#             form.save()
#             form = PostForm()
            
            
#     context = {'form': form}
#     return render(request, 'blog/create.html', context)
