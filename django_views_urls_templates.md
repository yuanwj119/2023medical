# Django视图、URL配置与模板系统指南

## 1. 博客应用的视图函数

在`blog_app/views.py`文件中添加以下代码来定义博客应用的视图函数和基于类的视图：

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Article, Author, Category, Tag, Comment
from .forms import CommentForm, ArticleForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect

# 基于函数的视图 - 首页视图
def home(request):
    # 获取已发布的文章，按发布时间倒序排列，只显示最新的6篇
    featured_articles = Article.objects.filter(status='published').order_by('-publish_time')[:6]
    
    # 获取热门分类
    categories = Category.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:5]
    
    # 获取热门标签
    tags = Tag.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:10]
    
    context = {
        'featured_articles': featured_articles,
        'categories': categories,
        'tags': tags,
        'page_title': '首页'
    }
    
    return render(request, 'blog_app/home.html', context)

# 基于类的视图 - 文章列表视图
class ArticleListView(ListView):
    model = Article
    template_name = 'blog_app/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # 每页显示10篇文章
    ordering = ['-publish_time']
    
    def get_queryset(self):
        # 只获取已发布的文章
        queryset = super().get_queryset().filter(status='published')
        
        # 搜索功能
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(author__name__icontains=search_query)
            )
        
        # 分类过滤
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # 标签过滤
        tag_slug = self.request.GET.get('tag', '')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '文章列表'
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        return context

# 基于类的视图 - 文章详情视图
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_app/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前文章的所有评论
        context['comments'] = self.object.comments.filter(is_approved=True).order_by('created_at')
        # 创建评论表单实例
        context['comment_form'] = CommentForm()
        context['page_title'] = self.object.title
        return context
    
    def post(self, request, *args, **kwargs):
        # 处理评论提交
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.save()
            messages.success(request, '评论已提交，等待审核！')
            return HttpResponseRedirect(self.object.get_absolute_url())
        
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)
    
    def get(self, request, *args, **kwargs):
        # 增加文章浏览量
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)

# 基于类的视图 - 分类列表视图
class CategoryListView(ListView):
    model = Category
    template_name = 'blog_app/category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 为每个分类添加文章数量
        for category in context['categories']:
            category.article_count = category.articles.filter(status='published').count()
        context['page_title'] = '文章分类'
        return context

# 基于类的视图 - 标签列表视图
class TagListView(ListView):
    model = Tag
    template_name = 'blog_app/tag_list.html'
    context_object_name = 'tags'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 为每个标签添加文章数量
        for tag in context['tags']:
            tag.article_count = tag.articles.filter(status='published').count()
        context['page_title'] = '文章标签'
        return context

# 基于类的视图 - 作者列表视图
class AuthorListView(ListView):
    model = Author
    template_name = 'blog_app/author_list.html'
    context_object_name = 'authors'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 为每个作者添加文章数量
        for author in context['authors']:
            author.article_count = author.articles.filter(status='published').count()
        context['page_title'] = '作者列表'
        return context

# 基于类的视图 - 作者详情视图
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog_app/author_detail.html'
    context_object_name = 'author'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前作者的已发布文章
        context['articles'] = self.object.articles.filter(status='published').order_by('-publish_time')[:5]
        context['page_title'] = f'{self.object.name}的主页'
        return context

# 自定义404错误视图
def custom_404(request, exception):
    return render(request, 'blog_app/404.html', status=404)

# 自定义500错误视图
def custom_500(request):
    return render(request, 'blog_app/500.html', status=500)

# 管理员视图 - 创建文章（需要登录和权限）
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'
    
    def form_valid(self, form):
        # 实际项目中需要设置当前登录用户关联的作者
        # form.instance.author = self.request.user.author
        messages.success(self.request, '文章创建成功！')
        return super().form_valid(form)

# 管理员视图 - 更新文章（需要登录和权限）
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, '文章更新成功！')
        return super().form_valid(form)
    
    def test_func(self):
        # 验证当前用户是否有权限编辑该文章
        article = self.get_object()
        # 实际项目中需要检查用户与作者的关联
        # return self.request.user.author == article.author
        return True  # 简化处理

# 管理员视图 - 删除文章（需要登录和权限）
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = reverse_lazy('article-list')
    
    def test_func(self):
        # 验证当前用户是否有权限删除该文章
        article = self.get_object()
        # 实际项目中需要检查用户与作者的关联
        # return self.request.user.author == article.author
        return True  # 简化处理
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '文章已成功删除！')
        return super().delete(request, *args, **kwargs)
```

## 2. 应用级别的URL配置（urls.py）

在`blog_app`目录下创建`urls.py`文件，并添加以下代码：

```python
from django.urls import path
from .views import (
    home,
    ArticleListView,
    ArticleDetailView,
    CategoryListView,
    TagListView,
    AuthorListView,
    AuthorDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
)

urlpatterns = [
    # 首页视图
    path('', home, name='home'),
    
    # 文章相关视图
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<slug:slug>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    
    # 分类相关视图
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # 标签相关视图
    path('tags/', TagListView.as_view(), name='tag-list'),
    
    # 作者相关视图
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
```

## 3. 项目级别的URL配置（blog_project/urls.py）

修改`blog_project/urls.py`文件，添加应用的URL配置：

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog_app.views import custom_404, custom_500

urlpatterns = [
    # 管理后台URL
    path('admin/', admin.site.urls),
    
    # 博客应用URL
    path('', include('blog_app.urls')),
]

# 在开发环境中提供媒体文件的服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 自定义错误视图
handler404 = custom_404
handler500 = custom_500
```

## 4. 表单定义（forms.py）

在`blog_app`目录下创建`forms.py`文件，并添加以下代码：

```python
from django import forms
from .models import Article, Comment

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '您的姓名'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '您的邮箱'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入评论内容', 'rows': 4}),
        }

class ArticleForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = Article
        fields = ('title', 'slug', 'content', 'author', 'category', 'tags', 'image', 'status', 'publish_time')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL标识符'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'publish_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
```

## 5. 模板系统的使用指南

### 5.1 模板目录结构

在`blog_app`目录下创建以下模板目录结构：

```
blog_app/
└── templates/
    └── blog_app/
        ├── base.html
        ├── home.html
        ├── article_list.html
        ├── article_detail.html
        ├── article_form.html
        ├── article_confirm_delete.html
        ├── category_list.html
        ├── tag_list.html
        ├── author_list.html
        ├── author_detail.html
        ├── 404.html
        └── 500.html
```

### 5.2 基础模板（base.html）

创建基础模板，包含网站的通用结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title|default:"博客网站" }}{% endblock %}</title>
    <!-- 引入Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <!-- 自定义样式 -->
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        .navbar {
            margin-bottom: 2rem;
        }
        .card {
            margin-bottom: 1.5rem;
            border: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .article-content {
            font-size: 1.1rem;
            line-height: 1.8;
        }
        .footer {
            margin-top: 4rem;
            padding: 2rem 0;
            background-color: #343a40;
            color: white;
        }
        .sidebar {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        .tag-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .tag-cloud a {
            text-decoration: none;
            padding: 0.3rem 0.8rem;
            background-color: #e9ecef;
            border-radius: 20px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        .tag-cloud a:hover {
            background-color: #0d6efd;
            color: white;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">博客网站</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">首页</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'article-list' %}">文章列表</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'category-list' %}">分类</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'tag-list' %}">标签</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'author-list' %}">作者</a>
                    </li>
                </ul>
                <!-- 搜索框 -->
                <form class="d-flex" action="{% url 'article-list' %}" method="get">
                    <input class="form-control me-2" type="search" placeholder="搜索文章" aria-label="Search" name="q">
                    <button class="btn btn-outline-light" type="submit">搜索</button>
                </form>
            </div>
        </div>
    </nav>

    <!-- 主内容区 -->
    <div class="container">
        <!-- 消息提示 -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        <div class="row">
            <!-- 主要内容 -->
            <div class="col-lg-8">
                {% block content %}{% endblock %}
            </div>
            
            <!-- 侧边栏 -->
            <div class="col-lg-4">
                <div class="sidebar mb-4">
                    <h4>热门分类</h4>
                    <ul class="list-group">
                        {% for category in categories %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <a href="{% url 'article-list' %}?category={{ category.slug }}">{{ category.name }}</a>
                                <span class="badge bg-primary rounded-pill">{{ category.article_count }}</span>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
                
                <div class="sidebar mb-4">
                    <h4>热门标签</h4>
                    <div class="tag-cloud">
                        {% for tag in tags %}
                            <a href="{% url 'article-list' %}?tag={{ tag.slug }}">{{ tag.name }}</a>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="sidebar">
                    <h4>最新文章</h4>
                    <ul class="list-group">
                        {% for article in featured_articles|slice:':5' %}
                            <li class="list-group-item">
                                <a href="{% url 'article-detail' article.slug %}">{{ article.title }}</a>
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container text-center">
            <p>&copy; {% now "Y" %} 博客网站 版权所有</p>
        </div>
    </footer>

    <!-- 引入Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 5.3 首页模板（home.html）

创建首页模板：

```html
{% extends 'blog_app/base.html' %}

{% block content %}
    <h1 class="mb-4">欢迎访问博客网站</h1>
    
    <div class="row">
        {% for article in featured_articles %}
            <div class="col-md-6">
                <div class="card">
                    {% if article.image %}
                        <img src="{{ article.image.url }}" class="card-img-top" alt="{{ article.title }}">
                    {% endif %}
                    <div class="card-body">
                        <span class="badge bg-primary mb-2">{{ article.category.name }}</span>
                        <h2 class="card-title h5"><a href="{% url 'article-detail' article.slug %}">{{ article.title }}</a></h2>
                        <p class="card-text text-muted">作者：<a href="{% url 'author-detail' article.author.id %}">{{ article.author.name }}</a> | 发布时间：{{ article.publish_time|date:"Y-m-d" }} | 浏览量：{{ article.view_count }} | 评论：{{ article.comments.count }}</p>
                        <p class="card-text">{{ article.content|striptags|truncatechars:100 }}</p>
                        <a href="{% url 'article-detail' article.slug %}" class="btn btn-primary">阅读更多</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <div class="col-12">
                <div class="alert alert-info" role="alert">
                    暂无文章
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

### 5.4 文章列表模板（article_list.html）

创建文章列表模板：

```html
{% extends 'blog_app/base.html' %}

{% block content %}
    <h1 class="mb-4">
        文章列表
        {% if current_category %} - <a href="{% url 'article-list' %}">分类：{{ categories|get:current_category }}</a>
        {% elif current_tag %} - <a href="{% url 'article-list' %}">标签：{{ tags|get:current_tag }}</a>
        {% endif %}
    </h1>
    
    {% if search_query %}
        <p class="text-muted mb-4">搜索结果："{{ search_query }}"（共 {{ page_obj.paginator.count }} 篇文章）</p>
    {% endif %}
    
    {% for article in articles %}
        <div class="card mb-4">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <span class="badge bg-primary">{{ article.category.name }}</span>
                    <span class="text-muted">{{ article.publish_time|date:"Y-m-d" }}</span>
                </div>
                <h2 class="card-title h4 mt-2"><a href="{% url 'article-detail' article.slug %}">{{ article.title }}</a></h2>
                <p class="card-text text-muted">作者：<a href="{% url 'author-detail' article.author.id %}">{{ article.author.name }}</a> | 浏览量：{{ article.view_count }} | 评论：{{ article.comments.count }}</p>
                <p class="card-text">{{ article.content|striptags|truncatechars:150 }}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="tag-cloud">
                        {% for tag in article.tags.all %}
                            <a href="{% url 'article-list' %}?tag={{ tag.slug }}">{{ tag.name }}</a>
                        {% endfor %}
                    </div>
                    <a href="{% url 'article-detail' article.slug %}" class="btn btn-primary">阅读更多</a>
                </div>
            </div>
        </div>
    {% empty %}
        <div class="alert alert-info" role="alert">
            没有找到符合条件的文章
        </div>
    {% endfor %}
    
    <!-- 分页 -->
    {% if is_paginated %}
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}{% if current_category %}&category={{ current_category }}{% endif %}{% if current_tag %}&tag={{ current_tag }}{% endif %}" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">&laquo;</span>
                    </li>
                {% endif %}
                
                {% for num in page_obj.paginator.page_range %}
                    {% if page_obj.number == num %}
                        <li class="page-item active"><span class="page-link">{{ num }}</span></li>
                    {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                        <li class="page-item"><a class="page-link" href="?page={{ num }}{% if search_query %}&q={{ search_query }}{% endif %}{% if current_category %}&category={{ current_category }}{% endif %}{% if current_tag %}&tag={{ current_tag }}{% endif %}">{{ num }}</a></li>
                    {% endif %}
                {% endfor %}
                
                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}{% if current_category %}&category={{ current_category }}{% endif %}{% if current_tag %}&tag={{ current_tag }}{% endif %}" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">&raquo;</span>
                    </li>
                {% endif %}
            </ul>
        </nav>
    {% endif %}
{% endblock %}
```

通过以上代码，您可以实现一个完整的Django博客应用的视图、URL配置和模板系统，为用户提供良好的浏览体验。