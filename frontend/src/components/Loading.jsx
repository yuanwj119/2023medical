import React from 'react'

function Loading({ message = '加载中...' }) {
  return (
    <div className="text-center mt-5">
      <div className="spinner-border" role="status">
        <span className="visually-hidden">加载中...</span>
      </div>
      <p className="mt-3">{message}</p>
    </div>
  )
}

export default Loading