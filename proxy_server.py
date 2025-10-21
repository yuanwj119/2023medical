from flask import Flask, jsonify, render_template_string

# 创建Flask应用
app = Flask(__name__)

# 模拟博客数据
mock_blogs = [
    {
        "id": 1,
        "title": "Django入门教程",
        "content": "这是一个Django入门教程，帮助你快速上手Django框架。",
        "author": "张老师",
        "created_at": "2025-01-15T10:00:00Z"
    },
    {
        "id": 2,
        "title": "Flask vs Django",
        "content": "本文对比了Flask和Django这两个流行的Python Web框架。",
        "author": "李教授",
        "created_at": "2025-02-20T14:30:00Z"
    },
    {
        "id": 3,
        "title": "Python Web开发最佳实践",
        "content": "分享Python Web开发中的一些最佳实践和技巧。",
        "author": "王工程师",
        "created_at": "2025-03-10T09:15:00Z"
    }
]

# 模拟作者数据
mock_authors = [
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
]

# 主页HTML模板
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客系统首页</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .blog-post {
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .blog-title {
            font-size: 1.5em;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .blog-meta {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        .blog-content {
            color: #34495e;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>欢迎来到博客系统</h1>
    <div class="blog-list">
        {% for blog in blogs %}
        <div class="blog-post">
            <h2 class="blog-title">{{ blog.title }}</h2>
            <div class="blog-meta">作者: {{ blog.author }} | 发布时间: {{ blog.created_at }}</div>
            <div class="blog-content">{{ blog.content }}</div>
        </div>
        {% endfor %}
    </div>
    <footer>
        <p>API文档：
            <a href="/api/blogs/">博客列表API</a> | 
            <a href="/api/authors/">作者列表API</a>
        </p>
    </footer>
</body>
</html>
'''

# 主页路由 - 显示博客列表
@app.route('/', methods=['GET'])
def home():
    return render_template_string(INDEX_HTML, blogs=mock_blogs)

# 博客列表API
@app.route('/api/blogs/', methods=['GET'])
def blog_list():
    return jsonify(mock_blogs)

# 博客详情API
@app.route('/api/blogs/<int:blog_id>/', methods=['GET'])
def blog_detail(blog_id):
    for blog in mock_blogs:
        if blog['id'] == blog_id:
            return jsonify(blog)
    return jsonify({"error": "Blog not found"}), 404

# 作者列表API
@app.route('/api/authors/', methods=['GET'])
def author_list():
    return jsonify(mock_authors)

# 作者详情API
@app.route('/api/authors/<int:author_id>/', methods=['GET'])
def author_detail(author_id):
    for author in mock_authors:
        if author['id'] == author_id:
            return jsonify(author)
    return jsonify({"error": "Author not found"}), 404

if __name__ == '__main__':
    # 启动Flask服务器
    print("Flask代理服务器启动中...")
    print("首页地址: http://127.0.0.1:8001/")
    print("API端点:")
    print("- 博客列表: http://127.0.0.1:8001/api/blogs/")
    print("- 作者列表: http://127.0.0.1:8001/api/authors/")
    app.run(host='0.0.0.0', port=8001, debug=True)