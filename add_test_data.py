import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog_app.models import Category, Article, Comment
from datetime import datetime, timedelta
import random

# 创建超级用户
def create_superuser():
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('超级用户已创建: admin/admin123')
        return admin_user
    else:
        print('超级用户已存在')
        return User.objects.get(username='admin')

# 创建普通用户
def create_users():
    users = []
    usernames = ['alice', 'bob', 'carol', 'david', 'eve']
    
    for username in usernames:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password=f'{username}123'
            )
            print(f'用户已创建: {username}')
            users.append(user)
        else:
            users.append(User.objects.get(username=username))
    
    return users

# 创建分类
def create_categories():
    categories = []
    category_names = ['技术', '生活', '旅行', '美食', '读书笔记', '编程']
    
    for name in category_names:
        if not Category.objects.filter(name=name).exists():
            category = Category.objects.create(name=name)
            print(f'分类已创建: {name}')
            categories.append(category)
        else:
            categories.append(Category.objects.get(name=name))
    
    return categories

# 创建文章
def create_articles(users, categories):
    articles = []
    article_titles = [
        'Django框架入门教程',
        'Python数据处理技巧分享',
        '如何提高编程效率',
        '周末旅行小记',
        '家常美食制作指南',
        '深度阅读《代码大全》',
        '前端开发新趋势',
        '数据库优化经验',
        '个人博客系统设计与实现',
        '机器学习入门笔记'
    ]
    
    article_contents = [
        '这是一篇关于Django框架的入门教程，主要介绍了Django的基本概念、项目结构和常用功能。通过本文的学习，读者可以快速上手Django开发。',
        '本文分享了Python数据处理中常用的一些技巧，包括数据清洗、转换、分析等方面的实用方法。适合数据分析师和Python开发者阅读。',
        '在日常开发中，如何提高编程效率是每个开发者都关心的问题。本文从工具使用、代码规范、工作习惯等方面给出了一些建议。',
        '上周末去了附近的一个小镇旅行，风景优美，人文气息浓厚。本文记录了这次旅行的见闻和感受。',
        '家常美食不一定复杂，本文分享了几道简单易做又美味的家常菜的制作方法，适合忙碌的上班族。',
        '《代码大全》是一本经典的编程书籍，本文分享了阅读这本书的一些心得和收获，以及对实际编程工作的影响。',
        'Web前端技术发展迅速，本文介绍了当前前端开发的一些新趋势和热门技术，包括框架、工具和方法论等方面。',
        '数据库性能对应用程序的整体性能影响很大。本文分享了一些数据库优化的经验和技巧，帮助开发者提高应用性能。',
        '本文详细介绍了个人博客系统的设计思路和实现过程，包括需求分析、数据库设计、功能模块划分等方面的内容。',
        '机器学习是当前热门的技术领域，本文作为入门笔记，介绍了机器学习的基本概念、常用算法和应用场景。'
    ]
    
    # 随机生成发布时间（过去30天内）
    today = datetime.now()
    
    for i in range(10):
        # 确保文章标题和内容一一对应
        title = article_titles[i]
        content = article_contents[i]
        
        # 如果文章已存在，则跳过
        if Article.objects.filter(title=title).exists():
            print(f'文章已存在: {title}')
            continue
        
        # 随机选择作者和分类
        author = random.choice(users)
        category = random.choice(categories)
        
        # 随机生成发布时间
        publish_days_ago = random.randint(0, 30)
        publish_time = today - timedelta(days=publish_days_ago)
        
        # 创建文章
        article = Article.objects.create(
            title=title,
            content=content,
            author=author,
            category=category,
            created_at=publish_time,
            updated_at=publish_time,
            is_published=True
        )
        
        print(f'文章已创建: {title} (作者: {author.username})')
        articles.append(article)
    
    return articles

# 创建评论
def create_comments(articles):
    comment_names = ['张三', '李四', '王五', '赵六', '钱七']
    comment_contents = [
        '非常棒的文章，学到了很多！',
        '感谢分享，期待更多精彩内容。',
        '有一些疑问，希望能进一步解释。',
        '这篇文章对我很有帮助，谢谢！',
        '写得很详细，初学者也能看懂。',
        '观点很独特，值得思考。',
        '内容丰富，实用性强。',
        '支持作者，继续加油！'
    ]
    
    for article in articles:
        # 为每篇文章添加1-3条评论
        num_comments = random.randint(1, 3)
        
        for _ in range(num_comments):
            # 随机选择评论者名称和评论内容
            name = random.choice(comment_names)
            content = random.choice(comment_contents)
            
            # 随机生成评论时间（在文章发布后）
            comment_days_after_publish = random.randint(0, 5)
            comment_time = article.created_at + timedelta(days=comment_days_after_publish)
            
            # 创建评论
            Comment.objects.create(
                article=article,
                name=name,
                email=f'{name.lower()}@example.com',
                content=content,
                created_at=comment_time
            )
            
        print(f'已为文章添加评论: {article.title}')

if __name__ == '__main__':
    print('开始添加测试数据...')
    
    # 创建超级用户
    admin_user = create_superuser()
    
    # 创建普通用户
    users = create_users()
    users.append(admin_user)  # 将超级用户也添加到用户列表
    
    # 创建分类
    categories = create_categories()
    
    # 创建文章
    articles = create_articles(users, categories)
    
    # 创建评论
    create_comments(articles)
    
    print('测试数据添加完成！')
    print('\n可以通过以下地址访问博客：')
    print('博客列表: http://127.0.0.1:8000/blogs/')
    print('作者列表: http://127.0.0.1:8000/authors/')
    print('管理后台: http://127.0.0.1:8000/admin/ (用户名: admin, 密码: admin123)')
    print('\n运行服务器命令: python manage.py runserver')