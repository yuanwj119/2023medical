from django.urls import path
from . import views

# 应用路由配置
urlpatterns = [
    # 根路由，指向index视图，返回前端页面
    path('', views.index, name='index'),
    # /posts路由，指向posts视图，返回JSON格式的帖子列表
    path('posts/', views.posts, name='posts'),
]