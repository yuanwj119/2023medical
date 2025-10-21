# Django项目模板和静态文件配置指南

本指南将帮助你在Django项目中配置templates目录和静态文件，使我们创建的`index.html`和`custom.css`文件能够正常工作。

## 创建templates目录

首先，在Django项目根目录下创建templates目录，并设置适当的权限：

```bash
# 进入blog_project目录
cd blog_project

# 创建templates目录
mkdir templates

# 在Windows系统上，权限设置通常不是必需的，如果你使用的是Linux/Mac系统，可以设置权限：
# chmod -R 755 templates
```

## 配置templates目录

需要在项目的`settings.py`文件中配置templates目录。打开`blog_project/settings.py`文件，找到`TEMPLATES`配置部分，修改如下：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加这一行
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

确保文件开头已经导入了`os`模块。如果没有，请添加：

```python
import os
```

## 创建静态文件目录结构

接下来，创建静态文件目录结构。Django项目通常有一个全局的静态文件目录和每个应用自己的静态文件目录。

```bash
# 在项目根目录下创建全局static目录
mkdir -p static/css static/js static/images

# 也可以在blog_app应用下创建静态文件目录
cd blog_app
mkdir -p static/blog_app/css static/blog_app/js static/blog_app/images
cd ..
```

## 配置静态文件

同样在`settings.py`文件中，找到或添加以下配置：

```python
# 静态文件配置
STATIC_URL = '/static/'

# 全局静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 运行collectstatic命令时，静态文件将被收集到这个目录
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 静态文件查找器
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

## 移动custom.css到正确位置

我们已经创建了`custom.css`文件，需要将它移动到静态文件目录中：

```bash
# 将custom.css移动到全局静态css目录
move ..\custom.css static\css\

# 或者，如果你使用的是Git Bash或Linux终端：
# mv ../custom.css static/css/
```

## 移动index.html到templates目录

同样，将`index.html`文件移动到templates目录：

```bash
# 将index.html移动到templates目录
move ..\index.html templates\

# 或者，如果你使用的是Git Bash或Linux终端：
# mv ../index.html templates/
```

## 配置视图以使用模板

要让首页能够访问，需要在`blog_app/views.py`中添加一个视图函数：

```python
from django.shortcuts import render

# 首页视图
def home(request):
    return render(request, 'index.html')
```

然后在`blog_app/urls.py`中添加对应的URL路由：

```python
from django.urls import path
from . import views

urlpatterns = [
    # 其他URL模式
    path('', views.home, name='home'),  # 添加首页路由
]
```

## 加载静态文件的标签

在Django模板中，我们使用`{% load static %}`标签来加载静态文件。确保你的`index.html`文件开头添加了这个标签：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的个人博客</title>
    <!-- 引入 Bootstrap 的 CSS 文件 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- 引入自定义的 CSS 文件 -->
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    <!-- 其他头部内容 -->
</head>
```

## 收集静态文件（部署时使用）

在部署Django项目时，需要运行`collectstatic`命令来收集所有静态文件到`STATIC_ROOT`目录：

```bash
python manage.py collectstatic
```

## 测试配置

完成上述配置后，运行开发服务器：

```bash
python manage.py runserver
```

然后在浏览器中访问 `http://127.0.0.1:8000/`，你应该能够看到美观的个人首页，并且样式已经正确应用。

## 常见问题排查

1. **模板未找到错误**：确保`templates`目录路径正确，并且在`settings.py`的`TEMPLATES['DIRS']`中正确配置。

2. **静态文件未加载**：检查`STATIC_URL`和`STATICFILES_DIRS`配置是否正确，确保模板中使用了`{% load static %}`标签，并且静态文件路径正确。

3. **权限问题**：在Linux/Mac系统上，确保目录和文件有正确的读写权限。

4. **Django版本兼容**：本指南适用于Django 3.x及以上版本。如果使用的是较早版本，可能需要调整某些配置。

通过以上步骤，你应该能够成功配置Django项目的模板和静态文件，使我们创建的个人首页能够正常运行。