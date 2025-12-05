from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment

# --- VERSÃO 1: Views Funcionais SEM Forms (Validação Manual) ---

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
    
    # Processamento manual do comentário (sem Form)
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
            return redirect('post_detail', pk=pk)

    return render(request, 'hub/post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        # Extração manual de dados
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_ids = request.POST.getlist('categories')
        
        # Criação do objeto
        post = Post.objects.create(title=title, content=content)
        
        # Associação ManyToMany manual
        if category_ids:
            for cat_id in category_ids:
                category = Category.objects.get(id=cat_id)
                post.categories.add(category)
        
        return redirect('post_list')
    
    categories = Category.objects.all()
    return render(request, 'hub/post_form.html', {'categories': categories})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        
        # Atualização ManyToMany manual
        category_ids = request.POST.getlist('categories')
        post.categories.clear()
        for cat_id in category_ids:
            post.categories.add(cat_id)
            
        return redirect('post_list')
        
    categories = Category.objects.all()
    return render(request, 'hub/post_form.html', {
        'post': post, # Para preencher o form manualmente no template se necessário
        'categories': categories
    })

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
