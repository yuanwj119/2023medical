/**
 * 无限滚动脚本
 * 功能：DOM加载完成后加载首批20条帖子，监听窗口滚动事件，当滚动到页面底部时加载下20条
 */

// 当前加载的起始位置
let currentStart = 0;
// 每次加载的数量
const batchSize = 20;
// 是否正在加载中，防止重复加载
let isLoading = false;

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 加载首批20条帖子（0-19）
    loadPosts(0, 19);
    
    // 监听窗口滚动事件
    window.addEventListener('scroll', handleScroll);
});

/**
 * 处理滚动事件，判断是否需要加载更多内容
 */
function handleScroll() {
    // 如果正在加载中，则不执行任何操作
    if (isLoading) return;
    
    // 检查是否滚动到了页面底部
    // window.innerHeight: 视窗高度
    // document.documentElement.scrollTop: 已滚动的高度
    // document.documentElement.offsetHeight: 整个文档的高度
    if (window.innerHeight + document.documentElement.scrollTop >= document.documentElement.offsetHeight - 100) {
        // 计算下一批的起始和结束位置
        const nextStart = currentStart + batchSize;
        const nextEnd = nextStart + batchSize - 1;
        
        // 加载下一批帖子
        loadPosts(nextStart, nextEnd);
    }
}

/**
 * 加载帖子
 * @param {number} start - 起始位置
 * @param {number} end - 结束位置
 */
function loadPosts(start, end) {
    // 设置为加载中状态
    isLoading = true;
    
    // 构建请求URL
    const url = `/posts?start=${start}&end=${end}`;
    
    // 使用fetch API请求数据
    fetch(url)
        .then(response => {
            // 检查响应是否成功
            if (!response.ok) {
                throw new Error('网络请求失败');
            }
            // 解析JSON响应
            return response.json();
        })
        .then(data => {
            // 获取posts容器
            const postsContainer = document.getElementById('posts');
            
            // 遍历返回的帖子列表
            data.posts.forEach(postText => {
                // 创建帖子元素
                const postElement = document.createElement('div');
                postElement.className = 'post';
                postElement.textContent = postText;
                
                // 添加到容器中
                postsContainer.appendChild(postElement);
            });
            
            // 更新当前起始位置
            currentStart = end + 1;
        })
        .catch(error => {
            console.error('加载帖子失败:', error);
        })
        .finally(() => {
            // 无论成功失败，都将加载状态设置为false
            isLoading = false;
        });
}