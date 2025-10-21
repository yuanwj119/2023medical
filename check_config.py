import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

# 尝试导入Django模块
import django
django.setup()

# 打印Django配置信息
from django.conf import settings
print(f"Django settings module: {settings.SETTINGS_MODULE}")
print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")

# 尝试导入URLconf模块
from django.urls import get_resolver
resolver = get_resolver()
print("URL patterns:")
for pattern in resolver.url_patterns:
    print(f"  - {pattern.pattern}")