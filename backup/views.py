from django.shortcuts import render
from django.http import HttpResponse

def show_student_info(request):
    """显示学生信息的视图函数"""
    student_info = {
        'name': '袁雯静',
        'student_id': '20231201010'
    }
    # 渲染模板并返回响应
    return render(request, 'backup/student_info.html', {'student_info': student_info})