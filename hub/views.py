from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment
from .forms import CommentForm, SignUpForm, PostForm

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'hub/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_comments'] = Comment.objects.select_related('author', 'post').order_by('-created_at')[:3]
        return context

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'hub/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().select_related('author')
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(self.request.get_full_path())
        
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'hub/post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'hub/post_form.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'hub/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Category
    template_name = 'hub/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'hub/category_detail.html'
    context_object_name = 'category'

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
