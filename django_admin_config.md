# Django管理后台配置与使用指南

## 1. 在admin.py中注册模型并自定义管理界面

在`blog_app/admin.py`文件中添加以下代码来注册模型并自定义管理后台显示：

```python
from django.contrib import admin
from .models import Author, Category, Tag, Article, Comment
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import SimpleListFilter
from django.db.models import Count

# 自定义过滤器 - 文章状态过滤器
class ArticleStatusFilter(SimpleListFilter):
    title = '文章状态'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return (
            ('draft', '草稿'),
            ('published', '已发布'),
        )
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(status=self.value())
        return queryset

# 自定义过滤器 - 作者过滤器
class AuthorFilter(SimpleListFilter):
    title = '作者'
    parameter_name = 'author'
    
    def lookups(self, request, model_admin):
        authors = Author.objects.all()
        return [(author.id, author.name) for author in authors]
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(author_id=self.value())
        return queryset

# 评论内联编辑
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # 默认不显示额外的空表单
    readonly_fields = ('created_at',)  # 将创建时间设为只读
    fields = ('name', 'email', 'content', 'is_approved', 'created_at')

# 文章模型的管理类
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('title', 'author', 'category', 'status', 'publish_time', 'view_count', 'created_at', 'comment_count')
    
    # 可点击进入编辑页的字段
    list_display_links = ('title',)
    
    # 列表页可编辑的字段
    list_editable = ('status',)
    
    # 过滤器
    list_filter = (ArticleStatusFilter, AuthorFilter, 'category', 'tags', 'created_at', 'publish_time')
    
    # 搜索字段
    search_fields = ('title', 'content', 'author__name', 'category__name')
    
    # 日期分层
    date_hierarchy = 'publish_time'
    
    # 排序方式
    ordering = ('-publish_time', '-created_at')
    
    # 编辑页字段分组
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('内容与状态', {
            'fields': ('content', 'image', 'status', 'publish_time')
        }),
        ('统计信息', {
            'fields': ('view_count',),
            'classes': ('collapse',)  # 可折叠
        }),
    )
    
    # 内联编辑关联模型
    inlines = [CommentInline]
    
    # 自动填充slug字段
    prepopulated_fields = {'slug': ('title',)}
    
    # 自定义列表显示字段
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = '评论数'
    comment_count.admin_order_field = 'comments_count'  # 允许排序
    
    # 自定义保存方法
    def save_model(self, request, obj, form, change):
        # 如果是新增文章且未指定作者，设置当前登录用户为作者
        if not change and not obj.author:
            # 实际项目中需要确保request.user与Author模型关联
            # 这里简化处理，假设已有作者
            pass
        super().save_model(request, obj, form, change)
    
    # 查询集重写，添加注释计数以便排序
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(comments_count=Count('comments'))

# 作者模型的管理类
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'article_count', 'display_avatar')
    list_display_links = ('name',)
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    fields = ('name', 'bio', 'email', 'avatar')
    readonly_fields = ('created_at', 'updated_at')
    
    # 自定义列表显示字段
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = '文章数'
    
    # 显示头像缩略图
    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return '无'
    display_avatar.short_description = '头像'

# 分类模型的管理类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    # 自定义列表显示字段
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = '文章数'

# 标签模型的管理类
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    # 自定义列表显示字段
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = '文章数'

# 评论模型的管理类
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'content_preview', 'is_approved', 'created_at')
    list_display_links = ('name',)
    list_filter = ('is_approved', 'created_at', 'article__author')
    search_fields = ('name', 'email', 'content', 'article__title')
    list_editable = ('is_approved',)
    
    # 显示评论内容预览
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'
    
    # 动作：批准所选评论
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'已批准 {updated} 条评论')
    approve_comments.short_description = '批准所选评论'

# 自定义管理站点标题和头部
admin.site.site_title = '博客管理系统'
admin.site.site_header = '博客管理系统'
admin.site.index_title = '欢迎使用博客管理系统'
```

## 2. 启动开发服务器并访问管理后台的指令

### 2.1 创建超级用户

在访问管理后台之前，需要先创建一个超级用户：

```bash
# 进入项目目录
cd c:\Users\27956\Desktop\blog\blog_project

# 创建超级用户
python manage.py createsuperuser
```

执行上述命令后，系统会提示您输入用户名、电子邮箱和密码。请按照提示完成输入。

### 2.2 启动开发服务器

创建超级用户后，启动Django开发服务器：

```bash
# 启动开发服务器
python manage.py runserver
```

默认情况下，开发服务器会在 http://127.0.0.1:8000/ 启动。

### 2.3 访问管理后台

在浏览器中访问以下URL来进入Django管理后台：

```
http://127.0.0.1:8000/admin/
```

使用您刚才创建的超级用户账号和密码登录管理后台。

## 3. 管理后台功能说明

### 3.1 文章管理

在管理后台中，您可以：

- **查看所有文章**：在文章列表页面可以看到所有文章的标题、作者、分类、状态等信息
- **搜索文章**：使用搜索框可以根据标题、内容、作者名称等搜索文章
- **筛选文章**：使用过滤器可以按状态、作者、分类、标签和日期筛选文章
- **快速编辑**：在列表页可以直接修改文章状态
- **详细编辑**：点击文章标题进入编辑页面，可以修改文章的所有信息
- **查看评论**：在文章编辑页面可以查看和管理该文章的所有评论

### 3.2 作者管理

- **查看所有作者**：可以查看所有作者的基本信息
- **添加/编辑作者**：可以添加新作者或编辑现有作者的信息
- **查看作者文章数量**：在列表页可以看到每个作者发表的文章数量
- **查看头像**：如果作者有上传头像，可以在列表页看到头像缩略图

### 3.3 分类和标签管理

- **查看所有分类/标签**：可以查看所有分类和标签
- **添加/编辑分类/标签**：可以添加新的分类和标签或编辑现有分类和标签
- **查看关联文章数量**：可以看到每个分类和标签关联的文章数量
- **自动生成URL标识符**：在添加/编辑分类和标签时，slug字段会根据名称自动生成

### 3.4 评论管理

- **查看所有评论**：可以查看所有评论的基本信息
- **搜索和筛选评论**：可以根据评论者名称、邮箱、评论内容、文章标题等搜索和筛选评论
- **批准/拒绝评论**：可以在列表页快速批准或拒绝评论
- **批量操作**：可以选择多条评论进行批量批准操作

## 4. 自定义管理后台的常见技巧

### 4.1 添加自定义动作

您可以为模型管理类添加自定义动作，例如上面代码中的批准评论功能：

```python
actions = ['approve_comments']

def approve_comments(self, request, queryset):
    updated = queryset.update(is_approved=True)
    self.message_user(request, f'已批准 {updated} 条评论')
approve_comments.short_description = '批准所选评论'
```

### 4.2 自定义列表显示

您可以添加自定义方法来显示模型中不存在但需要展示的信息：

```python
def comment_count(self, obj):
    return obj.comments.count()
comment_count.short_description = '评论数'
```

### 4.3 使用HTML格式化显示

使用`format_html`函数可以在管理后台中显示HTML内容，如显示图片：

```python
def display_avatar(self, obj):
    if obj.avatar:
        return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
    return '无'
display_avatar.short_description = '头像'
```

### 4.4 自定义过滤器

创建自定义过滤器可以提供更灵活的筛选功能：

```python
class ArticleStatusFilter(SimpleListFilter):
    title = '文章状态'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return (
            ('draft', '草稿'),
            ('published', '已发布'),
        )
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(status=self.value())
        return queryset
```

通过以上配置，您可以拥有一个功能强大、界面友好的Django管理后台，方便地管理博客应用的所有内容。