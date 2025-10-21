# 博客系统前端

使用React开发的博客系统前端界面。

## 技术栈

- React 18
- React Router 6
- Bootstrap 5
- Axios
- Vite

## 项目结构

```
frontend/
├── public/            # 静态资源
├── src/
│   ├── components/    # 通用组件
│   ├── pages/         # 页面组件
│   ├── services/      # API服务
│   ├── App.jsx        # 应用主组件
│   ├── main.jsx       # 入口文件
│   └── index.css      # 全局样式
├── index.html         # HTML模板
├── package.json       # 项目配置
└── vite.config.js     # Vite配置
```

## 安装依赖

```bash
# 进入frontend目录
cd frontend

# 安装依赖
npm install
```

## 运行项目

```bash
# 开发模式运行
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 主要功能

1. **博客列表**：显示所有博客文章，支持点击查看详情
2. **博客详情**：显示单篇文章内容和评论
3. **作者列表**：显示所有作者信息，包括文章数量和最新文章

## API接口

前端通过以下API接口与后端通信：

- `GET /api/blogs/` - 获取博客列表
- `GET /api/blogs/{id}/` - 获取博客详情
- `GET /api/authors/` - 获取作者列表

## 注意事项

1. 确保Django后端服务正在运行
2. 开发模式下，Vite配置了代理，将API请求转发到Django服务器
3. 生产环境部署时，需要配置正确的后端API地址