from django.shortcuts import render, get_object_or_404
from .models import Article, Author


def blog_list_view(request):
    """
    博客列表视图：获取所有博客文章数据，传递给模板并渲染
    
    参数:
        request: HTTP请求对象
        
    返回值:
        渲染后的HTML响应，包含所有博客文章数据
    
    功能说明:
        1. 从数据库中获取所有博客文章对象
        2. 按照发布时间倒序排列，确保最新的文章显示在前面
        3. 将文章数据打包成上下文字典
        4. 渲染博客列表模板并返回响应
    """
    # 获取所有博客文章，按发布时间倒序排列
    articles = Article.objects.all().order_by('-publish_time')
    
    # 准备上下文数据，传递给模板
    context = {
        'articles': articles,  # 文章列表
        'page_title': '博客列表'  # 页面标题
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/blog_list.html', context)


def blog_detail_view(request, article_id):
    """
    博客详情视图：根据文章ID获取单篇博客文章数据，传递给模板并渲染
    
    参数:
        request: HTTP请求对象
        article_id: 博客文章的ID
        
    返回值:
        渲染后的HTML响应，包含指定ID的博客文章数据
        如果文章不存在，返回404错误页面
        
    功能说明:
        1. 根据提供的article_id从数据库中获取对应的博客文章
        2. 如果文章不存在，自动返回404错误
        3. 将文章数据打包成上下文字典
        4. 渲染博客详情模板并返回响应
    """
    # 根据ID获取文章，如果不存在则返回404错误
    article = get_object_or_404(Article, pk=article_id)
    
    # 准备上下文数据，传递给模板
    context = {
        'article': article,  # 单个文章对象
        'page_title': article.title  # 使用文章标题作为页面标题
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/blog_detail.html', context)


def author_list_view(request):
    """
    作者列表视图：获取所有作者数据，传递给模板并渲染
    
    参数:
        request: HTTP请求对象
        
    返回值:
        渲染后的HTML响应，包含所有作者数据
        
    功能说明:
        1. 从数据库中获取所有作者对象
        2. 按照姓名字母顺序排列作者
        3. 为每个作者计算其发表的文章数量
        4. 将作者数据和文章数量打包成上下文字典
        5. 渲染作者列表模板并返回响应
    """
    # 获取所有作者，按姓名字母顺序排列
    authors = Author.objects.all().order_by('name')
    
    # 为每个作者添加文章数量属性
    for author in authors:
        # 计算每个作者发表的文章数量
        author.article_count = author.articles.count()
    
    # 准备上下文数据，传递给模板
    context = {
        'authors': authors,  # 作者列表
        'page_title': '作者列表'  # 页面标题
    }
    
    # 渲染模板并返回响应
    return render(request, 'blog_app/author_list.html', context)