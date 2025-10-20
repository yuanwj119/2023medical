from django.shortcuts import render
from django.http import JsonResponse
import time

# Create your views here.

def index(request):
    """
    首页视图，返回前端页面
    该视图负责渲染index.html模板，提供无限滚动的前端界面
    """
    return render(request, 'posts/index.html')

def posts(request):
    """
    帖子API视图，接收start和end参数，返回JSON格式的帖子列表
    
    Args:
        request: HTTP请求对象
        
    Returns:
        JsonResponse: 包含帖子列表的JSON响应，格式为{"posts": [帖子列表]}
    """
    # 获取URL参数，设置默认值
    try:
        start = int(request.GET.get('start', 0))
        # 如果没有提供end参数，则默认返回start到start+9的10条数据
        end = int(request.GET.get('end', start + 9))
        
        # 确保参数有效
        if start < 0 or end < start:
            start = 0
            end = start + 9
            
    except ValueError:
        # 处理非整数参数的情况
        start = 0
        end = 9
    
    # 模拟网络延迟
    time.sleep(1)
    
    # 生成帖子列表
    posts_list = [f"Post #{i}" for i in range(start, end + 1)]
    
    # 返回JSON响应
    return JsonResponse({"posts": posts_list})
