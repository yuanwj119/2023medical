import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAuthors } from '../services/api.js'

function AuthorList() {
  const [authors, setAuthors] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        setLoading(true)
        const data = await getAuthors()
        setAuthors(data)
      } catch (err) {
        setError('获取作者列表失败')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchAuthors()
  }, [])

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
        <p className="mt-3">加载作者列表中...</p>
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
        <h1 className="text-center">作者列表</h1>
        <hr />
      </header>

      <main>
        {authors.length > 0 ? (
          <div className="row">
            {authors.map((author) => (
              <div key={author.id} className="col-md-6 col-lg-4">
                <div className="card author-card">
                  <div className="author-info">
                    <h2 className="card-title">{author.username}</h2>
                    {author.email && (
                      <p className="text-muted">{author.email}</p>
                    )}
                    
                    <p>文章数量: <span className="badge bg-primary">{author.article_count}</span></p>
                    
                    {author.latest_article && (
                      <p>最新文章: 
                        <Link to={`/blog/${author.latest_article.id}`} className="text-primary">
                          {author.latest_article.title}
                        </Link>
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="alert alert-info text-center">
            <p>暂无作者信息</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default AuthorList