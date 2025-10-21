import React from 'react'
import { Link } from 'react-router-dom'

function ErrorMessage({ message = '发生错误', showHomeLink = true }) {
  return (
    <div className="alert alert-danger text-center mt-5">
      <p>{message}</p>
      {showHomeLink && (
        <div className="mt-3">
          <Link to="/" className="btn btn-primary">返回首页</Link>
        </div>
      )}
    </div>
  )
}

export default ErrorMessage