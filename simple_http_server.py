# 使用Python标准库创建的简单HTTP服务器
import http.server
import socketserver
import json

# 博客列表数据（不预先转换为JSON，便于后续处理单个博客）
BLOGS = [
    {
        "id": 1,
        "title": "Django入门教程",
        "content": "这是一个Django入门教程，帮助你快速上手Django框架。在本教程中，我们将学习Django的基本概念，包括模型、视图、模板等核心组件。",
        "detailed_content": "# Django入门教程\n\n## 什么是Django？\nDjango是一个高级Python Web框架，鼓励快速开发和干净、实用的设计。它由经验丰富的开发人员构建，解决了Web开发中的许多常见问题，因此您可以专注于编写应用程序，而无需重新发明轮子。\n\n## Django的核心组件\n- **模型(Models)**: 定义数据结构，与数据库交互\n- **视图(Views)**: 处理用户请求，返回响应\n- **模板(Templates)**: 定义页面的展示方式\n- **URLs**: 映射URL到对应的视图函数\n- **表单(Forms)**: 处理用户输入数据\n\n## 环境搭建\n1. 安装Python\n2. 安装Django: `pip install django`\n3. 创建项目: `django-admin startproject myproject`\n4. 运行开发服务器: `python manage.py runserver`\n\n## 创建第一个应用\n```python\npython manage.py startapp myapp\n```\n\n## 基本流程\n1. 定义模型\n2. 创建视图\n3. 设计模板\n4. 配置URLs\n5. 数据库迁移\n6. 测试应用\n\n## 总结\n通过本教程，您已经了解了Django的基本概念和开发流程。接下来，您可以开始构建自己的Django应用程序，探索更多高级功能。",
        "author": "张老师",
        "created_at": "2025-01-15T10:00:00Z",
        "category": "Web开发",
        "tags": ["Django", "Python", "Web开发"]
    },
    {
        "id": 2,
        "title": "Flask vs Django",
        "content": "本文对比了Flask和Django这两个流行的Python Web框架，帮助开发者选择适合自己项目的框架。",
        "detailed_content": "# Flask vs Django: 选择合适的Python Web框架\n\n## Flask: 微框架\nFlask被称为微框架，因为它保持了核心功能的简洁性，同时提供了扩展的灵活性。\n\n### 优点\n- **轻量级**: 核心代码简洁，启动快速\n- **灵活性**: 开发者可以自由选择组件\n- **学习曲线平缓**: 入门门槛低\n- **适合小型项目和API**: 构建简单服务的理想选择\n\n### 缺点\n- **需要手动选择和集成组件**: ORM、表单处理等需要额外安装\n- **大型项目可能需要更多配置**: 随着项目规模增长，需要更多自定义配置\n\n## Django: 全功能框架\nDjango是一个全功能的Web框架，遵循\"包含电池\"的理念，提供了开发所需的大部分组件。\n\n### 优点\n- **全功能**: ORM、管理后台、表单处理等内置功能\n- **安全性高**: 内置防XSS、CSRF等安全机制\n- **适合大型项目**: 结构清晰，易于维护\n- **活跃的社区**: 丰富的第三方包和文档\n\n### 缺点\n- **相对重量级**: 核心包含许多功能，可能有性能开销\n- **学习曲线陡峭**: 概念较多，需要时间掌握\n- **约定大于配置**: 灵活性相对较低\n\n## 如何选择？\n- 如果项目较小，需要快速开发，且团队熟悉Python，可以考虑Flask\n- 如果项目较大，需要完善的功能支持，特别是管理后台，可以考虑Django\n- 考虑团队的技术背景和项目的长期维护需求\n\n## 总结\nFlask和Django各有优势，选择哪个框架取决于具体的项目需求、团队能力和个人偏好。无论选择哪个框架，都能构建出优秀的Web应用。",
        "author": "李教授",
        "created_at": "2025-02-20T14:30:00Z",
        "category": "技术对比",
        "tags": ["Flask", "Django", "Python", "框架对比"]
    },
    {
        "id": 3,
        "title": "Python Web开发最佳实践",
        "content": "分享Python Web开发中的一些最佳实践和技巧，帮助开发者编写高质量的Web应用。",
        "detailed_content": "# Python Web开发最佳实践\n\n## 代码组织\n- 遵循PEP 8编码规范\n- 使用虚拟环境隔离项目依赖\n- 合理的目录结构设计\n- 模块间低耦合，高内聚\n\n## 安全措施\n- 使用HTTPS\n- 密码加密存储（使用bcrypt等算法）\n- 防范SQL注入、XSS、CSRF等攻击\n- 验证和清理用户输入\n- 设置合适的权限控制\n\n## 性能优化\n- 使用缓存（Redis、Memcached等）\n- 数据库查询优化\n- 使用异步处理（如asyncio）处理耗时操作\n- 静态资源压缩和CDN加速\n- 代码性能分析和优化\n\n## 测试策略\n- 单元测试：测试单个函数或类\n- 集成测试：测试组件间的交互\n- 端到端测试：模拟用户操作\n- 使用pytest等测试框架\n- 持续集成CI/CD\n\n## 部署建议\n- 使用Docker容器化应用\n- 自动化部署流程\n- 监控和日志记录\n- 定期备份\n- 灰度发布策略\n\n## 其他建议\n- 编写清晰的文档\n- 使用版本控制（Git）\n- 代码审查\n- 关注安全性更新和依赖漏洞\n\n## 总结\n遵循这些最佳实践，可以帮助你构建更安全、更可靠、更易维护的Python Web应用。记住，最佳实践不是一成不变的，需要根据项目的具体情况进行调整和优化。",
        "author": "王工程师",
        "created_at": "2025-03-10T09:15:00Z",
        "category": "最佳实践",
        "tags": ["Python", "Web开发", "最佳实践"]
    },
    {
        "id": 4,
        "title": "Python异步编程指南",
        "content": "本文介绍Python中的异步编程，包括asyncio库的使用方法和实际应用场景。",
        "detailed_content": "# Python异步编程指南\n\n## 什么是异步编程？\n异步编程是一种编程模式，允许程序在等待某些操作（如I/O操作）完成时不被阻塞，可以继续执行其他任务。\n\n## asyncio简介\nasyncio是Python的异步I/O框架，提供了协程、事件循环、任务等核心组件。\n\n## 基本概念\n- **协程(Coroutine)**: 使用async def定义的函数\n- **事件循环(Event Loop)**: 负责调度和执行协程\n- **任务(Task)**: 对协程的封装，可以并发执行\n- **Future**: 表示异步操作的最终结果\n\n## 基本语法\n```python\nasync def hello():\n    print(\"Hello\")\n    await asyncio.sleep(1)\n    print(\"World\")\n\nasync def main():\n    await hello()\n\nasyncio.run(main())\n```\n\n## 并发任务\n```python\nasync def main():\n    task1 = asyncio.create_task(hello(1))\n    task2 = asyncio.create_task(hello(2))\n    await task1\n    await task2\n```\n\n## 实际应用场景\n- 网络爬虫：并发请求多个网页\n- Web服务器：处理并发请求\n- 数据库操作：非阻塞数据库查询\n- 文件I/O：并发读写多个文件\n\n## 常见陷阱\n- 避免在协程中使用阻塞操作\n- 注意异常处理\n- 理解asyncio的调度机制\n\n## 总结\n异步编程可以显著提高I/O密集型应用的性能。通过合理使用asyncio，你可以编写高效的并发代码，充分利用系统资源。",
        "author": "张老师",
        "created_at": "2025-04-05T16:45:00Z",
        "category": "Python进阶",
        "tags": ["Python", "异步编程", "asyncio"]
    },
    {
        "id": 5,
        "title": "Django REST framework入门",
        "content": "本文介绍如何使用Django REST framework构建RESTful API，包括序列化器、视图集等核心组件。",
        "detailed_content": "# Django REST framework入门\n\n## 什么是Django REST framework？\nDjango REST framework是Django的一个强大的工具包，用于构建Web API。它提供了序列化、视图、权限控制等功能，极大地简化了API开发过程。\n\n## 安装\n```bash\npip install djangorestframework\n```\n\n## 基本配置\n在Django项目的settings.py中添加：\n```python\nINSTALLED_APPS = [\n    # ...\n    'rest_framework',\n]\n\nREST_FRAMEWORK = {\n    'DEFAULT_PERMISSION_CLASSES': [\n        'rest_framework.permissions.AllowAny',\n    ],\n    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\n    'PAGE_SIZE': 10\n}\n```\n\n## 序列化器\n序列化器用于将复杂数据类型（如Django模型）转换为JSON等可传输格式。\n```python\nfrom rest_framework import serializers\nfrom .models import Post\n\nclass PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = ['id', 'title', 'content', 'created_at']\n```\n\n## 视图集\n视图集提供了一组相关的API端点。\n```python\nfrom rest_framework import viewsets\nfrom .models import Post\nfrom .serializers import PostSerializer\n\nclass PostViewSet(viewsets.ModelViewSet):\n    queryset = Post.objects.all()\n    serializer_class = PostSerializer\n```\n\n## URL配置\n```python\nfrom django.urls import path, include\nfrom rest_framework.routers import DefaultRouter\nfrom .views import PostViewSet\n\nrouter = DefaultRouter()\nrouter.register(r'posts', PostViewSet)\n\nurlpatterns = [\n    path('', include(router.urls)),\n]\n```\n\n## 测试API\nDRF提供了一个可浏览的API界面，访问配置的URL即可看到。\n\n## 总结\nDjango REST framework大大简化了RESTful API的开发过程。通过使用序列化器、视图集等组件，你可以快速构建功能完善的API。",
        "author": "李教授",
        "created_at": "2025-05-12T11:20:00Z",
        "category": "API开发",
        "tags": ["Django", "RESTful", "API", "Python"]
    },
    {
        "id": 6,
        "title": "Python数据分析入门",
        "content": "本文介绍Python数据分析的基本工具和方法，包括NumPy、Pandas等库的使用。",
        "detailed_content": "# Python数据分析入门\n\n## 数据分析工具包\n- **NumPy**: 用于数值计算的基础库\n- **Pandas**: 用于数据处理和分析的核心库\n- **Matplotlib**: 用于数据可视化\n- **Seaborn**: 基于Matplotlib的高级可视化库\n- **Scikit-learn**: 机器学习库\n\n## 安装必要的库\n```bash\npip install numpy pandas matplotlib seaborn scikit-learn jupyter\n```\n\n## NumPy基础\n```python\nimport numpy as np\n\n# 创建数组\narr = np.array([1, 2, 3, 4, 5])\n\n# 数组运算\nresult = arr * 2\n\n# 数组索引和切片\nsubset = arr[1:4]\n```\n\n## Pandas基础\n```python\nimport pandas as pd\n\n# 创建DataFrame\ndf = pd.DataFrame({\n    'name': ['Alice', 'Bob', 'Charlie'],\n    'age': [25, 30, 35],\n    'city': ['New York', 'London', 'Paris']\n})\n\n# 数据查看\nprint(df.head())\nprint(df.info())\nprint(df.describe())\n\n# 数据筛选\nadults = df[df['age'] >= 30]\n\n# 数据分组\ngrouped = df.groupby('city').mean()\n```\n\n## 数据可视化\n```python\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# 折线图\ndf.plot(kind='line', x='name', y='age')\nplt.show()\n\n# 柱状图\nsns.barplot(x='city', y='age', data=df)\nplt.show()\n\n# 散点图\nsns.scatterplot(x='name', y='age', data=df)\nplt.show()\n```\n\n## 数据分析流程\n1. 数据收集：获取数据\n2. 数据清洗：处理缺失值、异常值\n3. 数据探索：了解数据特征\n4. 数据分析：应用统计方法\n5. 数据可视化：展示分析结果\n6. 生成报告：总结发现\n\n## 总结\nPython提供了强大的数据分析工具，通过组合使用这些工具，你可以高效地进行数据处理、分析和可视化。无论是数据科学家、分析师还是开发人员，掌握这些技能都非常有价值。",
        "author": "王工程师",
        "created_at": "2025-06-23T14:10:00Z",
        "category": "数据分析",
        "tags": ["Python", "数据分析", "Pandas", "NumPy"]
    }
]

# 将博客列表转换为JSON
BLOGS_DATA = json.dumps(BLOGS)

# 作者列表JSON数据
AUTHORS_DATA = json.dumps([
    {
        "id": 1,
        "name": "张老师",
        "bio": "资深Django开发者，拥有5年Web开发经验。",
        "email": "zhang@example.com"
    },
    {
        "id": 2,
        "name": "李教授",
        "bio": "计算机科学教授，专注于Web框架研究。",
        "email": "li@example.com"
    },
    {
        "id": 3,
        "name": "王工程师",
        "bio": "全栈开发工程师，热衷于分享技术经验。",
        "email": "wang@example.com"
    }
])

# 生成博客列表HTML的函数
def generate_blog_list_html():
    # 生成博客列表项
    blog_items = []
    for blog in BLOGS:
        # 格式化日期
        date = blog['created_at'].split('T')[0]
        blog_items.append(f"""
        <div class="blog-post">
            <h2 class="blog-title"><a href="/blog/{blog['id']}">{blog['title']}</a></h2>
            <div class="blog-meta">作者: {blog['author']} | 发布时间: {date} | 分类: {blog['category']}</div>
            <div class="blog-content">{blog['content']}</div>
            <div class="blog-tags">
                标签: {', '.join([f'<span class="tag">{tag}</span>' for tag in blog['tags']])}
            </div>
        </div>
        """)
    
    # 组合完整HTML
    html = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>博客系统首页</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
                background-color: #f5f5f5;
            }}
            header {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .blog-post {{
                margin-bottom: 30px;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }}
            .blog-post:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .blog-title {{
                font-size: 1.8em;
                margin-bottom: 10px;
            }}
            .blog-title a {{
                color: #2c3e50;
                text-decoration: none;
                display: block;
                padding-bottom: 5px;
            }}
            .blog-title a:hover {{
                color: #3498db;
            }}
            .blog-meta {{
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }}
            .blog-content {{
                color: #34495e;
                margin-bottom: 15px;
                line-height: 1.8;
            }}
            .blog-tags {{
                margin-top: 10px;
            }}
            .tag {{
                display: inline-block;
                background-color: #ecf0f1;
                color: #7f8c8d;
                padding: 3px 10px;
                border-radius: 15px;
                font-size: 0.8em;
                margin-right: 5px;
                margin-bottom: 5px;
            }}
            footer {{
                text-align: center;
                margin-top: 50px;
                padding: 20px;
                color: #7f8c8d;
                border-top: 1px solid #eee;
            }}
            .back-to-home {{
                display: inline-block;
                margin-top: 20px;
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 0.9em;
            }}
            .back-to-home:hover {{
                background-color: #2980b9;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>欢迎来到博客系统</h1>
            <p>这里有最新的技术文章和教程，欢迎阅读和分享！</p>
        </header>
        <div class="blog-list">
            {''.join(blog_items)}
        </div>
        <footer>
            <p>共有 {len(BLOGS)} 篇文章 | 
                <a href="/api/blogs">博客列表API</a> | 
                <a href="/api/authors">作者列表API</a>
            </p>
        </footer>
    </body>
    </html>
    '''
    return html.encode('utf-8')

# 生成博客详情HTML的函数
def generate_blog_detail_html(blog_id):
    # 查找对应ID的博客
    blog = None
    for b in BLOGS:
        if b['id'] == blog_id:
            blog = b
            break
    
    if not blog:
        return '<html><body><h1>博客不存在</h1><p>您访问的博客不存在或已被删除。</p><a href="/" style="display: inline-block; margin-top: 20px; padding: 8px 15px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px;">返回首页</a></body></html>'.encode('utf-8')
    
    # 格式化日期
    date = blog['created_at'].split('T')[0]
    
    # 将Markdown格式的内容转换为简单的HTML
    content_html = blog['detailed_content']
    # 处理标题
    content_html = content_html.replace('# ', '<h1>').replace('\n# ', '\n<h1>')
    content_html = content_html.replace('\n<h1>', '</h1>\n<p>')
    content_html = content_html.replace('## ', '<h2>').replace('\n## ', '\n<h2>')
    content_html = content_html.replace('\n<h2>', '</h2>\n<p>')
    # 处理段落
    content_html = content_html.replace('\n\n', '</p>\n<p>')
    # 处理代码块（简单处理）
    content_html = content_html.replace('```python\n', '<pre><code class="python">')
    content_html = content_html.replace('```\n', '</code></pre>\n')
    
    html = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{blog['title']} - 博客系统</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
                background-color: #f5f5f5;
            }}
            .blog-detail {{
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                margin-top: 0;
                border-bottom: 2px solid #3498db;
                padding-bottom: 15px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }}
            .blog-meta {{
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid #eee;
            }}
            .blog-content {{
                color: #34495e;
                line-height: 1.8;
            }}
            .blog-content p {{
                margin-bottom: 20px;
            }}
            .blog-tags {{
                margin-top: 30px;
                padding-top: 15px;
                border-top: 1px solid #eee;
            }}
            .tag {{
                display: inline-block;
                background-color: #ecf0f1;
                color: #7f8c8d;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.8em;
                margin-right: 10px;
                margin-bottom: 10px;
            }}
            .back-to-home {{
                display: inline-block;
                margin-top: 30px;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 1em;
            }}
            .back-to-home:hover {{
                background-color: #2980b9;
            }}
            pre {{
                background-color: #f8f8f8;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}
            code {{
                font-family: Consolas, Monaco, 'Andale Mono', monospace;
                background-color: #f8f8f8;
                padding: 2px 4px;
                border-radius: 3px;
                font-size: 0.9em;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <div class="blog-detail">
            <h1>{blog['title']}</h1>
            <div class="blog-meta">
                作者: {blog['author']} | 
                发布时间: {date} | 
                分类: {blog['category']}
            </div>
            <div class="blog-content">
                <p>{content_html}</p>
            </div>
            <div class="blog-tags">
                标签: {', '.join([f'<span class="tag">{tag}</span>' for tag in blog['tags']])}
            </div>
            <a href="/" class="back-to-home">返回首页</a>
        </div>
    </body>
    </html>
    '''
    return html.encode('utf-8')

# 自定义HTTP请求处理器
class CustomHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 处理根路径 - 博客列表页
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(generate_blog_list_html())
        # 处理博客详情页
        elif self.path.startswith('/blog/'):
            try:
                # 提取博客ID
                blog_id = int(self.path.split('/')[2])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(generate_blog_detail_html(blog_id))
            except (ValueError, IndexError):
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('<html><body><h1>404 Not Found</h1><p>无效的博客ID</p><a href="/" style="display: inline-block; margin-top: 20px; padding: 8px 15px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px;">返回首页</a></body></html>'.encode('utf-8'))
        # 处理博客列表API
        elif self.path == '/api/blogs' or self.path == '/api/blogs/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(BLOGS_DATA.encode('utf-8'))
        # 处理单个博客API
        elif self.path.startswith('/api/blogs/') and len(self.path.split('/')) > 3:
            try:
                # 提取博客ID
                blog_id = int(self.path.split('/')[3])
                # 查找博客
                for blog in BLOGS:
                    if blog['id'] == blog_id:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(blog).encode('utf-8'))
                        return
                # 未找到博客
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "博客不存在"}).encode('utf-8'))
            except (ValueError, IndexError):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "无效的请求"}).encode('utf-8'))
        # 处理作者列表API
        elif self.path == '/api/authors' or self.path == '/api/authors/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(AUTHORS_DATA.encode('utf-8'))
        else:
            # 处理404错误
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><h1>404 Not Found</h1><p>页面不存在</p><a href="/">返回首页</a></body></html>'.encode('utf-8'))

    # 重写log_message方法，避免控制台输出过多信息
    def log_message(self, format, *args):
        return

# 启动服务器
if __name__ == '__main__':
    PORT = 8003
    print(f"简单HTTP服务器启动中...")
    print(f"首页地址: http://127.0.0.1:{PORT}/")
    print(f"功能说明:")
    print(f"- 首页显示所有博客列表，共 {len(BLOGS)} 篇文章")
    print(f"- 点击博客标题可以查看详情")
    print(f"API端点:")
    print(f"- 博客列表: http://127.0.0.1:{PORT}/api/blogs")
    print(f"- 单篇博客: http://127.0.0.1:{PORT}/api/blogs/<id>")
    print(f"- 作者列表: http://127.0.0.1:{PORT}/api/authors")
    
    # 创建服务器
    httpd = socketserver.TCPServer(("", PORT), CustomHTTPHandler)
    
    try:
        # 启动服务器
        httpd.serve_forever()
    except KeyboardInterrupt:
        # 处理Ctrl+C中断
        print("\n服务器正在关闭...")
        httpd.server_close()