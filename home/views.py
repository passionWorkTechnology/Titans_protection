from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment
from .forms import CommentForm, PostForm



def list_blog(request):
    posts = Post.objects.all().order_by('-created_at')  
    context = {
        'posts': posts
    }
    return render(request, "blog/blog_list.html", context)


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index')
    
    return render(request, 'blog/login.html', {'form': form})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    posts_count = posts.count()
    comments_count = Comment.objects.filter(post__author=request.user).count()
    
    return render(request, 'blog/dashboard.html', {
        'posts': posts,
        'posts_count': posts_count,
        'comments_count': comments_count
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('dashboard')