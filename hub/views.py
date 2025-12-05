from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

# --- VERSÃO 2: Views Funcionais COM Forms ---

def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    recent_comments = Comment.objects.select_related('author', 'post').order_by('-created_at')[:3]
    return render(request, 'hub/post_list.html', {
        'posts': posts,
        'categories': categories,
        'recent_comments': recent_comments
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().select_related('author')
    
    form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)

    return render(request, 'hub/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    
    return render(request, 'hub/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
        
    return render(request, 'hub/post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'hub/post_confirm_delete.html', {'object': post})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'hub/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'hub/category_detail.html', {'category': category})
