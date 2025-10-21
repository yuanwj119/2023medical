import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getBlogDetail } from '../services/api.js'

function BlogDetail() {
  const { id } = useParams()
  const [article, setArticle] = useState(null)
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchBlogDetail = async () => {
      try {
        setLoading(true)
        const data = await getBlogDetail(id)
        setArticle(data.article)
        setComments(data.comments)
      } catch (err) {
        setError('获取博客详情失败')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchBlogDetail()
  }, [id])

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
        <p className="mt-3">加载博客详情中...</p>
      </div>
    )
  }

  if (error || !article) {
    return (
      <div className="alert alert-danger text-center mt-5">
        {error || '博客不存在'}
        <div className="mt-3">
          <Link to="/" className="btn btn-primary">返回首页</Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <header className="mb-5">
        <h1 className="text-center">{article.title}</h1>
        <hr />
      </header>

      <main>
        <div className="article-info">
          <p><strong>作者:</strong> {article.author.username}</p>
          <p><strong>分类:</strong> {article.category.name}</p>
          <p><strong>创建时间:</strong> {new Date(article.created_at).toLocaleString('zh-CN')}</p>
          {article.updated_at !== article.created_at && (
            <p><strong>更新时间:</strong> {new Date(article.updated_at).toLocaleString('zh-CN')}</p>
          )}
          <p><strong>状态:</strong> {article.is_published ? '已发布' : '草稿'}</p>
        </div>

        <div className="article-content">
          {article.content.split('\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>

        <div className="mt-4">
          <Link to="/" className="btn btn-primary">返回博客列表</Link>
        </div>

        {/* 评论部分 */}
        <div className="comment-section">
          <h2>评论 ({comments.length})</h2>

          {comments.length > 0 ? (
            comments.map((comment) => (
              <div key={comment.id} className="comment">
                <p className="comment-author">
                  {comment.name} <span className="comment-date">
                    ({new Date(comment.created_at).toLocaleString('zh-CN')})
                  </span>
                </p>
                <p>{comment.content}</p>
              </div>
            ))
          ) : (
            <p className="text-center text-muted">暂无评论</p>
          )}
        </div>
      </main>
    </div>
  )
}

export default BlogDetail