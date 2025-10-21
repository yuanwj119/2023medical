import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import BlogList from './pages/BlogList.jsx'
import BlogDetail from './pages/BlogDetail.jsx'
import AuthorList from './pages/AuthorList.jsx'

function App() {
  return (
    <Router>
      <div className="container">
        {/* 导航栏 */}
        <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
          <div className="container-fluid">
            <Link to="/" className="navbar-brand">个人博客系统</Link>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link to="/" className="nav-link">博客首页</Link>
                </li>
                <li className="nav-item">
                  <Link to="/authors" className="nav-link">作者列表</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* 页面路由 */}
        <Routes>
          <Route path="/" element={<BlogList />} />
          <Route path="/blog/:id" element={<BlogDetail />} />
          <Route path="/authors" element={<AuthorList />} />
        </Routes>

        {/* 页脚 */}
        <footer className="mt-5 pt-5 border-top">
          <div className="text-center">
            <p>&copy; 2024 个人博客系统</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App