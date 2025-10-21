# Django博客项目创建与运行指南

## 重要提示
当前目录 `c:\Users\27956\Desktop\blog` 中只有指南文档和代码文件，**没有实际的Django项目结构**，因此无法直接运行 `manage.py runserver` 命令。

## 完整步骤指南

### 步骤1: 安装Django
首先确保已安装Django框架：

```powershell
pip install django
```

### 步骤2: 创建Django项目
在当前目录下创建Django项目：

```powershell
django-admin startproject blog_project .
```

**注意：** 命令末尾的 `.` 很重要，它表示在当前目录创建项目，而不是创建新目录。

### 步骤3: 创建博客应用
在项目中创建blog_app应用：

```powershell
python manage.py startapp blog_app
```

### 步骤4: 配置应用
编辑 `blog_project/settings.py` 文件，添加blog_app到INSTALLED_APPS：

```python
INSTALLED_APPS = [
    # Django自带应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自定义应用
    'blog_app',
]
```

### 步骤5: 创建模型
在 `blog_app/models.py` 文件中定义博客模型：

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.article.title}'
```

### 步骤6: 执行数据库迁移

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 步骤7: 创建超级用户

```powershell
python manage.py createsuperuser
```
按照提示输入用户名、邮箱和密码。

### 步骤8: 配置URL
1. 创建 `blog_app/urls.py` 文件：

```python
from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('blogs/', views.blog_list_view, name='blog_list'),
    path('blogs/<int:article_id>/', views.blog_detail_view, name='blog_detail'),
    path('authors/', views.author_list_view, name='author_list'),
]
```

2. 更新 `blog_project/urls.py` 文件：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),
]
```

### 步骤9: 创建视图
在 `blog_app/views.py` 文件中创建视图函数（可以使用已有的blog_app_views.py内容）：

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, User

# 博客列表视图
def blog_list_view(request):
    articles = Article.objects.all().order_by('-created_at')
    context = {'articles': articles}
    return render(request, 'blog_app/blog_list.html', context)

# 博客详情视图
def blog_detail_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    context = {'article': article}
    return render(request, 'blog_app/blog_detail.html', context)

# 作者列表视图
def author_list_view(request):
    authors = User.objects.all()
    context = {'authors': authors}
    return render(request, 'blog_app/author_list.html', context)
```

### 步骤10: 创建模板目录结构

```powershell
mkdir -p blog_app/templates/blog_app
```

创建简单的模板文件 `blog_app/templates/blog_app/blog_list.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>博客列表</title>
</head>
<body>
    <h1>博客文章列表</h1>
    {% for article in articles %}
        <h2><a href="{% url 'blog_app:blog_detail' article.id %}">{{ article.title }}</a></h2>
        <p>作者: {{ article.author.username }}</p>
        <p>发布时间: {{ article.created_at }}</p>
        <p>{{ article.content|truncatewords:50 }}</p>
        <hr>
    {% empty %}
        <p>暂无博客文章</p>
    {% endfor %}
</body>
</html>
```

### 步骤11: 创建静态文件目录

```powershell
mkdir -p blog_app/static/css
```

将已有的custom.css文件复制到该目录。

### 步骤12: 运行开发服务器
完成以上步骤后，就可以运行开发服务器了：

```powershell
python manage.py runserver
```

### 步骤13: 访问网站
打开浏览器，访问以下地址：
- 管理后台：http://127.0.0.1:8000/admin/
- 博客列表：http://127.0.0.1:8000/blogs/
- 作者列表：http://127.0.0.1:8000/authors/

## 常见问题排查
1. 找不到manage.py：确保已执行 `django-admin startproject blog_project .` 命令
2. 数据库迁移错误：检查models.py中的模型定义是否正确
3. URL错误：确保URL配置正确，特别是app_name和namespace的使用
4. 模板不存在：检查模板文件路径和名称是否正确

按照以上步骤操作，您将能够成功创建并运行Django博客项目！