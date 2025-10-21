from django.contrib import admin
from django.urls import path, include

# 项目的主URL配置
urlpatterns = [
    # 管理后台URL：/admin/ 路径将指向Django管理后台
    path('admin/', admin.site.urls),
    
    # 包含blog_app应用的URL配置
    # 所有以应用URL配置中定义的路径开头的请求都将被转发到blog_app应用
    path('', include('blog_app.urls')),
]