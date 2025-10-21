# Django博客项目完整实现指南

本指南将帮助您在Windows系统上，从创建Django项目开始，完成博客项目的所有必要配置，直到能够成功运行开发服务器。所有命令均适用于命令提示符（CMD）或PowerShell环境。

## 前提条件

- 已安装Python（我们之前已确认安装了Python 3.13.7）
- 已安装Django（我们之前已确认安装了Django 5.2.6）
- 当前工作目录：`c:\Users\27956\Desktop\blog`

## 第一步：创建Django项目

1. 打开命令提示符（CMD）或PowerShell
2. 确保当前目录是 `c:\Users\27956\Desktop\blog`
3. 执行以下命令创建Django项目：

```cmd
# 使用django-admin命令创建项目
python -m django startproject blog_project .
```

**注意**：命令末尾的`.`表示在当前目录创建项目，而不是创建新目录。

执行完命令后，您的目录结构应该是这样的：
```
blog/
├── blog_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── 其他指南文件...
```

## 第二步：创建blog_app应用

1. 在同一个命令窗口中，执行以下命令创建blog_app应用：

```cmd
# 创建blog_app应用
python manage.py startapp blog_app
```

创建完应用后，您的目录结构应该新增了blog_app目录：
```
blog/
├── blog_project/
├── blog_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── 其他指南文件...
```

2. 将blog_app添加到项目的已安装应用中。打开 `blog_project/settings.py` 文件，找到 `INSTALLED_APPS` 列表，添加 `'blog_app'`：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_app',  # 添加这一行
]
```

## 第三步：定义模型

1. 打开 `blog_app/models.py` 文件，定义博客文章和作者模型：

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 作者模型（如果需要扩展Django默认的User模型）
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    website = models.URLField(blank=True)
    social_media = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

# 博客文章模型
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='article_images/', blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    read_count = models.PositiveIntegerField(default=0)
    
    # 文章分类
    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
        ]
    
    def __str__(self):
        return self.title

# 文章分类模型
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    articles = models.ManyToManyField(Article, related_name='categories', blank=True)
    
    def __str__(self):
        return self.name

# 评论模型
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.name} on {self.article.title}'
```

2. 创建媒体文件存储目录（用于存储上传的图片）：

```cmd
# 创建媒体文件目录
mkdir -p media/profile_pics media/article_images
```

3. 在 `blog_project/settings.py` 中配置媒体文件路径：

```python
# 添加在文件末尾
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 第四步：创建和应用数据库迁移

1. 执行以下命令创建数据库迁移文件：

```cmd
# 创建迁移文件
python manage.py makemigrations
```

2. 应用数据库迁移：

```cmd
# 应用迁移
python manage.py migrate
```

## 第五步：创建超级用户

为了能够访问Django管理后台，需要创建一个超级用户：

```cmd
# 创建超级用户
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

## 第六步：配置管理后台

1. 打开 `blog_app/admin.py` 文件，注册模型：

```python
from django.contrib import admin
from .models import Author, Article, Category, Comment

# 自定义文章管理界面
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status', 'read_count')
    list_filter = ('status', 'publish_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    ordering = ('status', '-publish_date')
    actions = ['approve_articles']
    
    def approve_articles(self, request, queryset):
        queryset.update(status=True)
    
    approve_articles.short_description = "批准选中的文章"

# 自定义作者管理界面
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
    
# 自定义分类管理界面
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# 自定义评论管理界面
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    
    approve_comments.short_description = "批准选中的评论"
```

## 第七步：创建视图

1. 打开 `blog_app/views.py` 文件，添加视图函数：

```python
from django.shortcuts import render, get_object_or_404
from .models import Article, Author, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 博客列表视图
def blog_list_view(request):
    # 获取所有已发布的文章，并按发布日期倒序排列
    articles_list = Article.objects.filter(status=True).order_by('-publish_date')
    
    # 添加分页功能，每页显示5篇文章
    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，显示第一页
        articles = paginator.page(1)
    except EmptyPage:
        # 如果page超出范围，显示最后一页
        articles = paginator.page(paginator.num_pages)
    
    # 准备上下文数据
    context = {
        'articles': articles,
        'page': page
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/article_list.html', context)

# 博客详情视图
def blog_detail_view(request, article_id):
    # 获取指定ID的文章，不存在则返回404错误
    article = get_object_or_404(Article, id=article_id, status=True)
    
    # 更新文章阅读量
    article.read_count += 1
    article.save()
    
    # 获取文章的评论（只显示已批准的评论）
    comments = article.comments.filter(approved=True)
    
    # 准备上下文数据
    context = {
        'article': article,
        'comments': comments
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/article_detail.html', context)

# 作者列表视图
def author_list_view(request):
    # 获取所有作者
    authors = Author.objects.all().order_by('user__username')
    
    # 准备上下文数据
    context = {
        'authors': authors
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/author_list.html', context)

# 首页视图
def home(request):
    # 获取最新的5篇文章
    latest_articles = Article.objects.filter(status=True).order_by('-publish_date')[:5]
    
    # 获取所有分类
    categories = Category.objects.all()
    
    # 准备上下文数据
    context = {
        'latest_articles': latest_articles,
        'categories': categories
    }
    
    # 渲染模板并返回响应
    return render(request, 'index.html', context)
```

## 第八步：配置URL

1. 在 `blog_app` 目录下创建 `urls.py` 文件：

```cmd
# 创建urls.py文件
cd blog_app
notepad urls.py
```

在打开的编辑器中输入以下内容，然后保存并关闭：

```python
from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    # 博客列表
    path('blogs/', views.blog_list_view, name='blog_list'),
    # 博客详情
    path('blogs/<int:article_id>/', views.blog_detail_view, name='blog_detail'),
    # 作者列表
    path('authors/', views.author_list_view, name='author_list'),
]
```

2. 更新项目的 `blog_project/urls.py` 文件：

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 第九步：配置模板和静态文件

1. 创建项目级别的模板目录：

```cmd
# 返回项目根目录
cd ..
# 创建templates目录
mkdir templates
# 创建blog_app的模板目录
mkdir templates/blog_app
```

2. 在 `blog_project/settings.py` 中配置模板目录：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加这一行
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

3. 创建静态文件目录结构：

```cmd
# 创建全局静态文件目录
mkdir -p static/css static/js static/images
# 创建blog_app的静态文件目录
mkdir -p blog_app/static/blog_app/css blog_app/static/blog_app/js
```

4. 在 `blog_project/settings.py` 中配置静态文件：

```python
# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

5. 将之前创建的 `index.html` 复制到 `templates` 目录：

```cmd
# 复制index.html到templates目录
copy index.html templates\
```

6. 修改 `templates/index.html` 文件，添加Django模板标签：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的个人博客</title>
    <!-- 引入 Bootstrap 的 CSS 文件 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- 引入自定义的 CSS 文件 -->
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    <!-- 引入 Font Awesome 图标库 -->
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
</head>
<!-- 其他内容保持不变 -->
</html>
```

7. 将之前创建的 `custom.css` 复制到静态文件目录：

```cmd
# 复制custom.css到static/css目录
copy custom.css static\css\
```

8. 创建博客列表和详情模板：

创建 `templates/blog_app/article_list.html` 文件：
```html
{% extends 'base.html' %}
{% block content %}
    <div class="container mt-8">
        <h1 class="text-3xl font-bold mb-6">博客文章</h1>
        
        {% for article in articles %}
            <div class="mb-8">
                <h2 class="text-xl font-semibold mb-2">
                    <a href="{% url 'blog_app:blog_detail' article.id %}">{{ article.title }}</a>
                </h2>
                <p class="text-gray-600 mb-2">作者: {{ article.author }} | 发布日期: {{ article.publish_date }}</p>
                <p class="mb-4">{{ article.excerpt|default:article.content|truncatewords:30 }}</p>
                <a href="{% url 'blog_app:blog_detail' article.id %}" class="btn btn-primary">阅读更多</a>
            </div>
        {% empty %}
            <p>暂无博客文章</p>
        {% endfor %}
        
        <!-- 分页导航 -->
        <div class="mt-8">
            {% if articles.has_previous %}
                <a href="?page={{ articles.previous_page_number }}" class="btn btn-outline-primary">上一页</a>
            {% endif %}
            
            <span class="mx-2">第 {{ articles.number }} 页，共 {{ articles.paginator.num_pages }} 页</span>
            
            {% if articles.has_next %}
                <a href="?page={{ articles.next_page_number }}" class="btn btn-outline-primary">下一页</a>
            {% endif %}
        </div>
    </div>
{% endblock %}
```

创建 `templates/blog_app/article_detail.html` 文件：
```html
{% extends 'base.html' %}
{% block content %}
    <div class="container mt-8">
        <h1 class="text-3xl font-bold mb-4">{{ article.title }}</h1>
        <p class="text-gray-600 mb-6">作者: {{ article.author }} | 发布日期: {{ article.publish_date }} | 阅读数: {{ article.read_count }}</p>
        
        {% if article.featured_image %}
            <img src="{{ article.featured_image.url }}" alt="{{ article.title }}" class="img-fluid mb-6">
        {% endif %}
        
        <div class="content mb-8">
            {{ article.content|safe }}
        </div>
        
        <!-- 评论区 -->
        <div class="mt-12">
            <h2 class="text-2xl font-bold mb-6">评论 ({{ comments.count }})</h2>
            
            <!-- 评论列表 -->
            <div class="mb-8">
                {% for comment in comments %}
                    <div class="mb-4 p-4 bg-gray-50 rounded">
                        <p class="font-semibold">{{ comment.name }}</p>
                        <p class="text-gray-600 text-sm mb-2">{{ comment.created_at }}</p>
                        <p>{{ comment.content }}</p>
                    </div>
                {% empty %}
                    <p>暂无评论，来发表第一条评论吧！</p>
                {% endfor %}
            </div>
        </div>
    </div>
{% endblock %}
```

创建 `templates/blog_app/author_list.html` 文件：
```html
{% extends 'base.html' %}
{% block content %}
    <div class="container mt-8">
        <h1 class="text-3xl font-bold mb-6">作者列表</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for author in authors %}
                <div class="p-4 border rounded">
                    {% if author.profile_picture %}
                        <img src="{{ author.profile_picture.url }}" alt="{{ author.user.username }}" class="w-24 h-24 rounded-full mb-4">
                    {% endif %}
                    <h2 class="text-xl font-semibold mb-2">{{ author.user.username }}</h2>
                    {% if author.bio %}
                        <p class="text-gray-600 mb-4">{{ author.bio|truncatewords:20 }}</p>
                    {% endif %}
                    <div>
                        <a href="#" class="btn btn-primary">查看文章</a>
                    </div>
                </div>
            {% empty %}
                <p>暂无作者</p>
            {% endfor %}
        </div>
    </div>
{% endblock %}
```

创建 `templates/base.html` 文件（作为基础模板）：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}我的个人博客{% endblock %}</title>
    <!-- 引入 Bootstrap 的 CSS 文件 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- 引入自定义的 CSS 文件 -->
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    <!-- 引入 Font Awesome 图标库 -->
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'blog_app:home' %}">
                <i class="fa fa-pencil-square-o" aria-hidden="true"></i> 我的博客
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == '/' %}active{% endif %}" href="{% url 'blog_app:home' %}">首页</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == '/blogs/' %}active{% endif %}" href="{% url 'blog_app:blog_list' %}">博客文章</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == '/authors/' %}active{% endif %}" href="{% url 'blog_app:author_list' %}">作者</a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="/admin/">管理后台</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">退出登录</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="#">登录</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- 主要内容 -->
    <main class="pt-20 pb-10">
        {% block content %}
        {% endblock %}
    </main>

    <!-- 页脚 -->
    <footer class="bg-dark text-white py-10">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-6">
                    <h3 class="text-xl mb-4">关于我的博客</h3>
                    <p>这是我的个人博客，我会在这里分享我的技术心得、编程经验和生活感悟。欢迎关注我的博客，与我一起交流学习！</p>
                </div>
                <div class="col-lg-4 col-md-6 mb-6">
                    <h3 class="text-xl mb-4">快速链接</h3>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="{% url 'blog_app:home' %}" class="text-gray-300 hover:text-white transition-colors duration-300">首页</a></li>
                        <li class="mb-2"><a href="{% url 'blog_app:blog_list' %}" class="text-gray-300 hover:text-white transition-colors duration-300">博客文章</a></li>
                        <li class="mb-2"><a href="{% url 'blog_app:author_list' %}" class="text-gray-300 hover:text-white transition-colors duration-300">作者</a></li>
                        {% if user.is_authenticated %}
                            <li class="mb-2"><a href="/admin/" class="text-gray-300 hover:text-white transition-colors duration-300">管理后台</a></li>
                        {% endif %}
                    </ul>
                </div>
                <div class="col-lg-4 mb-6">
                    <h3 class="text-xl mb-4">订阅我的博客</h3>
                    <p>订阅我的博客更新，第一时间获取最新的技术分享和文章推送。</p>
                    <form class="mt-4">
                        <div class="input-group">
                            <input type="email" class="form-control" placeholder="请输入您的邮箱地址">
                            <button type="submit" class="btn btn-primary">订阅</button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-12 text-center pt-6 border-t border-gray-700">
                    <p>&copy; 2023 我的个人博客. 保留所有权利.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- 返回顶部按钮 -->
    <button id="backToTop" class="btn btn-primary fixed-bottom-right p-3 rounded-full shadow-lg opacity-0 invisible transition-all duration-300 z-50">
        <i class="fa fa-arrow-up" aria-hidden="true"></i>
    </button>

    <!-- 引入 Bootstrap 的 JavaScript 文件 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- 自定义 JavaScript -->
    <script>
        // 页面滚动监听，显示/隐藏返回顶部按钮
        window.addEventListener('scroll', function() {
            const backToTopBtn = document.getElementById('backToTop');
            if (window.scrollY > 300) {
                backToTopBtn.classList.remove('opacity-0', 'invisible');
                backToTopBtn.classList.add('opacity-100', 'visible');
            } else {
                backToTopBtn.classList.remove('opacity-100', 'visible');
                backToTopBtn.classList.add('opacity-0', 'invisible');
            }
        });

        // 返回顶部功能
        document.getElementById('backToTop').addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // 导航栏滚动效果
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('nav');
            if (window.scrollY > 100) {
                navbar.classList.add('bg-dark/95', 'shadow-lg');
                navbar.classList.remove('bg-dark');
            } else {
                navbar.classList.remove('bg-dark/95', 'shadow-lg');
                navbar.classList.add('bg-dark');
            }
        });
    </script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 第十步：添加测试数据

为了能够看到效果，我们可以使用Django的shell添加一些测试数据：

```cmd
# 启动Django shell
python manage.py shell
```

在shell中输入以下代码添加测试数据：

```python
from django.contrib.auth.models import User
from blog_app.models import Author, Article, Category
import datetime

# 创建一个用户
user = User.objects.create_user(username='admin', email='admin@example.com', password='admin123')
user.is_staff = True
user.is_superuser = True
user.save()

# 创建对应的作者
author = Author.objects.create(user=user, bio='Django开发者', website='https://example.com')

# 创建几个分类
category1 = Category.objects.create(name='Python')
category2 = Category.objects.create(name='Django')
category3 = Category.objects.create(name='Web开发')

# 创建几篇测试文章
article1 = Article.objects.create(
    title='Django入门指南',
    slug='django-intro-guide',
    author=author,
    content='这是一篇关于Django入门的详细指南，适合初学者阅读。Django是一个高级Python Web框架，它鼓励快速开发和干净、实用的设计。',
    excerpt='Django入门指南，适合初学者阅读。',
    publish_date=datetime.datetime.now() - datetime.timedelta(days=1)
)
article1.categories.add(category1, category2)

article2 = Article.objects.create(
    title='Python高级特性',
    slug='python-advanced-features',
    author=author,
    content='本文介绍Python的一些高级特性，包括装饰器、生成器、上下文管理器等。掌握这些特性可以让你的Python代码更加优雅和高效。',
    excerpt='Python的高级特性介绍。',
    publish_date=datetime.datetime.now() - datetime.timedelta(days=2)
)
article2.categories.add(category1)

article3 = Article.objects.create(
    title='现代Web开发趋势',
    slug='modern-web-development-trends',
    author=author,
    content='本文探讨当前Web开发领域的最新趋势，包括前后端分离、微服务架构、容器化部署等。了解这些趋势有助于你更好地规划和构建现代Web应用。',
    excerpt='现代Web开发的最新趋势分析。',
    publish_date=datetime.datetime.now() - datetime.timedelta(days=3)
)
article3.categories.add(category3)

# 退出shell
exit()
```

## 第十一步：运行开发服务器

现在，所有配置都已完成，您可以运行开发服务器来查看效果：

```cmd
# 运行开发服务器
python manage.py runserver
```

服务器启动后，您可以在浏览器中访问以下URL：
- 博客首页：http://127.0.0.1:8000/
- 博客文章列表：http://127.0.0.1:8000/blogs/
- 作者列表：http://127.0.0.1:8000/authors/
- Django管理后台：http://127.0.0.1:8000/admin/（使用之前创建的超级用户账号登录）

## 后续步骤

1. **完善模型**：根据需求进一步完善博客模型
2. **添加表单**：实现评论表单、搜索功能等
3. **用户认证**：添加用户注册、登录功能
4. **优化视图**：添加基于类的视图、API等
5. **部署项目**：准备部署到生产环境

通过以上步骤，您已经成功创建了一个基本的Django博客项目，并能够正常运行开发服务器。祝您的博客项目开发顺利！