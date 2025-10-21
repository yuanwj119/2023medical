# Django模型创建、数据迁移与测试数据添加指南

## 1. 博客文章和作者的模型类代码

在`blog_app/models.py`文件中，添加以下代码来定义博客文章和作者的模型类：

```python
from django.db import models
from django.utils import timezone

class Author(models.Model):
    """作者模型"""
    name = models.CharField(max_length=100, verbose_name='姓名')
    bio = models.TextField(blank=True, verbose_name='简介')
    email = models.EmailField(blank=True, verbose_name='电子邮箱')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'
        ordering = ['-created_at']

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL标识符')
    description = models.TextField(blank=True, verbose_name='分类描述')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

class Tag(models.Model):
    """文章标签模型"""
    name = models.CharField(max_length=50, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL标识符')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

class Article(models.Model):
    """博客文章模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique_for_date='publish_time', verbose_name='URL标识符')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='标签')
    image = models.ImageField(upload_to='article_images/', blank=True, null=True, verbose_name='封面图片')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    publish_time = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    
    def save(self, *args, **kwargs):
        # 如果文章状态为已发布且未设置发布时间，则设置为当前时间
        if self.status == 'published' and not self.publish_time:
            self.publish_time = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-publish_time', '-created_at']

class Comment(models.Model):
    """文章评论模型"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    name = models.CharField(max_length=100, verbose_name='评论者名称')
    email = models.EmailField(verbose_name='评论者邮箱')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    is_approved = models.BooleanField(default=True, verbose_name='是否已批准')
    
    def __str__(self):
        return f'{self.name} 评论了 {self.article.title}'
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']
```

## 2. 使用Django数据迁移创建数据表的指令

### 2.1 在settings.py中注册应用

首先，确保在`blog_project/settings.py`中注册了`blog_app`应用：

```python
INSTALLED_APPS = [
    # Django内置应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方应用
    
    # 自定义应用
    'blog_app',
]
```

### 2.2 执行数据迁移命令

在终端中执行以下命令来创建和应用数据库迁移：

```bash
# 进入项目目录
cd c:\Users\27956\Desktop\blog\blog_project

# 创建迁移文件
python manage.py makemigrations blog_app

# 应用迁移，创建数据表
python manage.py migrate
```

## 3. 通过Django shell添加测试数据的代码示例

### 3.1 启动Django shell

在终端中执行以下命令来启动Django shell：

```bash
cd c:\Users\27956\Desktop\blog\blog_project
python manage.py shell
```

### 3.2 添加测试数据的代码

在Django shell中执行以下代码来添加测试数据：

```python
# 导入模型类
from blog_app.models import Author, Category, Tag, Article
from django.utils import timezone
import datetime

# 创建作者
author1 = Author.objects.create(
    name='张三',
    bio='资深程序员，热爱分享技术心得。',
    email='zhangsan@example.com'
)

author2 = Author.objects.create(
    name='李四',
    bio='全栈开发者，专注于Web开发和移动应用。',
    email='lisi@example.com'
)

# 创建分类
category1 = Category.objects.create(
    name='技术博客',
    slug='tech',
    description='分享编程技术和开发经验'
)

category2 = Category.objects.create(
    name='生活随笔',
    slug='life',
    description='记录生活点滴和感悟'
)

# 创建标签
tag1 = Tag.objects.create(name='Python', slug='python')
tag2 = Tag.objects.create(name='Django', slug='django')
tag3 = Tag.objects.create(name='Web开发', slug='web-development')
tag4 = Tag.objects.create(name='生活', slug='life')

# 创建博客文章
article1 = Article.objects.create(
    title='Django入门教程：从零开始构建博客网站',
    slug='django-beginner-tutorial',
    content='''
# Django入门教程

在本教程中，我们将学习如何使用Django框架从零开始构建一个博客网站。

## 什么是Django？
Django是一个高级Python Web框架，它鼓励快速开发和干净、实用的设计。

## 为什么选择Django？
- 内置管理后台
- ORM数据库抽象
- 模板系统
- URL路由
- 用户认证和权限系统

## 开始创建项目
首先，我们需要安装Django并创建一个新的项目...
''',
    author=author1,
    category=category1,
    status='published',
    publish_time=timezone.now() - datetime.timedelta(days=3)
)
article1.tags.add(tag1, tag2, tag3)

article2 = Article.objects.create(
    title='Python装饰器的艺术',
    slug='python-decorators-art',
    content='''
# Python装饰器的艺术

装饰器是Python中一个非常强大且有用的工具，它允许程序员修改函数或类的行为。

## 装饰器基础
装饰器本质上是一个返回函数的函数。

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

## 实际应用场景
- 日志记录
- 性能分析
- 权限验证
- 缓存

通过本文，我们深入探讨了Python装饰器的使用方法和应用场景...
''',
    author=author1,
    category=category1,
    status='published',
    publish_time=timezone.now() - datetime.timedelta(days=7)
)
article2.tags.add(tag1, tag3)

article3 = Article.objects.create(
    title='程序员的高效工作方式',
    slug='productive-programming',
    content='''
# 程序员的高效工作方式

作为程序员，如何提高工作效率是我们不断追求的目标。以下是一些提高效率的方法：

## 1. 自动化重复性工作
- 使用脚本自动化部署流程
- 设置开发环境自动化配置
- 使用代码生成工具减少重复编码

## 2. 合理安排时间
- 番茄工作法
- 避免多任务处理
- 充分利用碎片时间

## 3. 持续学习
- 阅读技术博客和书籍
- 参与开源项目
- 定期参加技术会议

通过这些方法，我成功将工作效率提高了50%...
''',
    author=author2,
    category=category1,
    status='published',
    publish_time=timezone.now() - datetime.timedelta(days=10)
)
article3.tags.add(tag3)

article4 = Article.objects.create(
    title='周末游记：探索郊外的自然风光',
    slug='weekend-trip',
    content='''
# 周末游记：探索郊外的自然风光

上周末，我和朋友们一起去郊外徒步，探索了美丽的自然风光。

## 准备工作
- 背包、水、食物
- 合适的徒步鞋和衣物
- 地图和指南针
- 急救包

## 行程安排
- 第一天：出发，到达目的地，搭建营地
- 第二天：徒步探索，欣赏风景
- 第三天：返回城市

## 收获与感悟
这次旅行让我暂时远离了城市的喧嚣，重新连接了自然，也让我思考了生活的意义...
''',
    author=author2,
    category=category2,
    status='published',
    publish_time=timezone.now() - datetime.timedelta(days=15)
)
article4.tags.add(tag4)

article5 = Article.objects.create(
    title='Django REST framework入门指南',
    slug='django-rest-framework-guide',
    content='''
# Django REST framework入门指南

Django REST framework是一个功能强大且灵活的工具包，用于构建Web API。

## 为什么选择DRF？
- 序列化功能，支持ORM和非ORM数据源
- 丰富的文档支持
- 身份验证和权限管理
- 强大的视图系统
- 扩展性强

## 安装与配置
```bash
pip install djangorestframework
```

然后在settings.py中添加到INSTALLED_APPS...
''',
    author=author1,
    category=category1,
    status='draft'  # 草稿状态
)
article5.tags.add(tag1, tag2, tag3)

# 验证数据是否创建成功
print(f"创建了 {Author.objects.count()} 位作者")
print(f"创建了 {Category.objects.count()} 个分类")
print(f"创建了 {Tag.objects.count()} 个标签")
print(f"创建了 {Article.objects.count()} 篇文章")
print(f"其中已发布的文章有: {Article.objects.filter(status='published').count()} 篇")
```

### 3.3 退出Django shell

完成测试数据添加后，可以使用以下命令退出Django shell：

```python
exit()
```

## 4. 常用的Django ORM查询示例

以下是一些常用的Django ORM查询示例，可以在Django shell中使用：

```python
# 获取所有已发布的文章
published_articles = Article.objects.filter(status='published')

# 获取特定作者的文章
author_articles = Article.objects.filter(author__name='张三')

# 获取特定分类的文章
category_articles = Article.objects.filter(category__name='技术博客')

# 获取包含特定标签的文章
tag_articles = Article.objects.filter(tags__name='Python')

# 获取最近发布的5篇文章
latest_articles = Article.objects.filter(status='published').order_by('-publish_time')[:5]

# 获取文章数量统计
article_count = Article.objects.count()

# 获取某个作者的文章数量
author_article_count = Article.objects.filter(author__name='张三').count()
```

通过以上步骤，您可以成功创建Django模型、执行数据迁移并添加测试数据，为开发博客应用打下基础。