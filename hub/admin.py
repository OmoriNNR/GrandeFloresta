from django.contrib import admin
from .models import Category, Post, Comment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at', 'categories')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'has_media')
    list_filter = ('created_at',)

    @admin.display(boolean=True, description='Mídia?')
    def has_media(self, obj):
        return bool(obj.media)
