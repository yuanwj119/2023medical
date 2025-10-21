import os
import sys

# 确保项目根目录在Python路径中
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# 明确设置Django设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'

# 导入Django并设置
import django
django.setup()

# 打印配置信息用于调试
from django.conf import settings
print(f"Using settings: {settings.SETTINGS_MODULE}")
print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")

# 尝试导入URLconf模块来验证
from django.urls import get_resolver
try:
    resolver = get_resolver()
    print("Successfully loaded URLconf")
except Exception as e:
    print(f"Error loading URLconf: {e}")

# 启动开发服务器
from django.core.management.commands.runserver import Command as RunserverCommand

if __name__ == '__main__':
    command = RunserverCommand()
    # 使用默认参数启动服务器
    command.execute("0.0.0.0:8000")