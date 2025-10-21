from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Article, Comment
import json

# 博客列表视图
def blog_list_view(request):
    # 如果是API请求，返回JSON格式数据
    if request.path.startswith('/api/'):
        # 获取所有文章，按创建时间倒序排列
        articles = Article.objects.all().order_by('-created_at')
        # 构建文章数据列表
        articles_data = []
        for article in articles:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': {
                    'id': article.author.id,
                    'username': article.author.username,
                },
                'created_at': article.created_at.isoformat() if article.created_at else None,
                'updated_at': article.updated_at.isoformat() if article.updated_at else None
            })
        # 返回JSON响应
        return JsonResponse(articles_data, safe=False)
    else:
        # 原来的HTML渲染逻辑
        articles = Article.objects.all().order_by('-created_at')
        context = {
            'articles': articles,  # 文章列表
            'page_title': '博客列表'  # 页面标题
        }
        # 渲染模板并返回响应
        return render(request, 'blog_app/blog_list.html', context)

# 博客详情视图
def blog_detail_view(request, article_id):
    # 如果是API请求，返回JSON格式数据
    if request.path.startswith('/api/'):
        # 根据ID获取文章，如果不存在则返回404错误
        article = get_object_or_404(Article, pk=article_id)
        
        # 获取该文章的所有评论
        comments = article.comment_set.all().order_by('created_at')
        
        # 构建评论数据列表
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.isoformat() if comment.created_at else None
            })
        
        # 构建文章详情数据
        article_data = {
            'article': {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': {
                    'id': article.author.id,
                    'username': article.author.username,
                },
                'created_at': article.created_at.isoformat() if article.created_at else None,
                'updated_at': article.updated_at.isoformat() if article.updated_at else None
            },
            'comments': comments_data
        }
        
        # 返回JSON响应
        return JsonResponse(article_data)
    else:
        # 原来的HTML渲染逻辑
        # 根据ID获取文章，如果不存在则返回404错误
        article = get_object_or_404(Article, pk=article_id)
        
        # 获取该文章的所有评论
        comments = article.comment_set.all().order_by('created_at')
        
        # 准备上下文数据，传递给模板
        context = {
            'article': article,  # 单个文章对象
            'comments': comments,  # 文章的评论列表
            'page_title': article.title  # 使用文章标题作为页面标题
        }
        
        # 渲染模板并返回响应
        return render(request, 'blog_app/blog_detail.html', context)

# 作者列表视图
def author_list_view(request):
    # 如果是API请求，返回JSON格式数据
    if request.path.startswith('/api/'):
        # 获取所有作者，按用户名字母顺序排列
        authors = User.objects.all().order_by('username')
        
        # 构建作者数据列表
        authors_data = []
        for author in authors:
            # 获取该作者的文章数量
            article_count = author.article_set.count()
            
            # 获取该作者的最新文章
            latest_article = author.article_set.order_by('-created_at').first()
            latest_article_data = None
            if latest_article:
                latest_article_data = {
                    'id': latest_article.id,
                    'title': latest_article.title
                }
            
            authors_data.append({
                'id': author.id,
                'username': author.username,
                'article_count': article_count,
                'latest_article': latest_article_data
            })
        
        # 返回JSON响应
        return JsonResponse(authors_data, safe=False)
    else:
        # 原来的HTML渲染逻辑
        # 获取所有作者，按用户名字母顺序排列
        authors = User.objects.all().order_by('username')
        
        # 准备上下文数据，传递给模板
        context = {
            'authors': authors,  # 作者列表
            'page_title': '作者列表'  # 页面标题
        }
        
        # 渲染模板并返回响应
        return render(request, 'blog_app/author_list.html', context)
