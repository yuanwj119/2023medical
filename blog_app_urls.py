from django.urls import path
from . import views

# 应用名称，用于URL命名空间
app_name = 'blog_app'

# URL模式列表，将URL路径与视图函数关联
urlpatterns = [
    # 博客列表视图：/blogs/ 路径将调用blog_list_view函数
    path('blogs/', views.blog_list_view, name='blog_list'),
    
    # 博客详情视图：/blogs/<int:pk>/ 路径将调用blog_detail_view函数
    # <int:pk>是URL参数，用于传递文章的主键ID
    path('blogs/<int:article_id>/', views.blog_detail_view, name='blog_detail'),
    
    # 作者列表视图：/authors/ 路径将调用author_list_view函数
    path('authors/', views.author_list_view, name='author_list'),
]