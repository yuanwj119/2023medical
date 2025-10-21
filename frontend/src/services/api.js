import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 获取博客列表
export const getBlogs = async () => {
  try {
    const response = await api.get('/blogs/')
    return response.data
  } catch (error) {
    console.error('获取博客列表失败:', error)
    throw error
  }
}

// 获取博客详情
export const getBlogDetail = async (id) => {
  try {
    const response = await api.get(`/blogs/${id}/`)
    return response.data
  } catch (error) {
    console.error('获取博客详情失败:', error)
    throw error
  }
}

// 获取作者列表
export const getAuthors = async () => {
  try {
    const response = await api.get('/authors/')
    return response.data
  } catch (error) {
    console.error('获取作者列表失败:', error)
    throw error
  }
}

export default api