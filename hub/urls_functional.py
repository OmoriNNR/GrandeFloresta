from django.urls import path
from . import views

# Este arquivo de URLs serve tanto para a Versão 1 quanto para a Versão 2 (Views Funcionais)
# Para usar, substitua o conteúdo de hub/urls.py por este.

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]
