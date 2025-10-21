import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getBlogs } from '../services/api.js'

function BlogList() {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        setLoading(true)
        const data = await getBlogs()
        setArticles(data)
      } catch (err) {
        setError('获取博客列表失败')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchBlogs()
  }, [])

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
        <p className="mt-3">加载博客列表中...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="alert alert-danger text-center mt-5">
        {error}
      </div>
    )
  }

  return (
    <div>
      <header className="mb-5">
        <h1 className="text-center">博客文章列表</h1>
        <hr />
      </header>

      <main>
        {articles.length > 0 ? (
          <div className="row">
            {articles.map((article) => (
              <div key={article.id} className="col-md-6 col-lg-4">
                <div className="card article-card">
                  <div className="card-body">
                    <h2 className="card-title">
                      <Link to={`/blog/${article.id}`} className="text-decoration-none">
                        {article.title}
                      </Link>
                    </h2>
                    <p className="article-date">
                      作者: {article.author.username} | 创建时间: {new Date(article.created_at).toLocaleString('zh-CN')}
                    </p>
                    <p className="card-text">
                      {article.content.substring(0, 150)}...
                    </p>
                    <Link to={`/blog/${article.id}`} className="btn btn-primary">
                      阅读全文
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="alert alert-info text-center">
            <p>暂无博客文章</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default BlogList