from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # 根路径路由，指向博客列表页面
    path('', views.blog_list_view, name='home'),
    # 原来的页面路由
    path('blogs/', views.blog_list_view, name='blog_list'),
    path('blogs/<int:article_id>/', views.blog_detail_view, name='blog_detail'),
    path('authors/', views.author_list_view, name='author_list'),
    
    # API路由 - 用于前端React应用调用
    path('api/blogs/', views.blog_list_view, name='api_blog_list'),
    path('api/blogs/<int:article_id>/', views.blog_detail_view, name='api_blog_detail'),
    path('api/authors/', views.author_list_view, name='api_author_list'),
]