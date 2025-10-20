from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def index(request):
    """返回前端页面"""
    return render(request, 'main/index.html')

def section(request, num):
    """根据传入的整数返回对应文本"""
    if num not in [1, 2, 3]:
        return HttpResponse(status=404)
    
    # 根据num值返回相应文本
    content_map = {
        1: "这是页面1的后端内容",
        2: "这是页面2的后端内容",
        3: "这是页面3的后端内容"
    }
    
    return HttpResponse(content_map[num])
