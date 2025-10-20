function showPage(pageNum) {
    // 隐藏所有页面内容
    const pages = document.querySelectorAll('.page-content');
    pages.forEach(page => {
        page.style.display = 'none';
    });
    
    // 显示选中的页面
    const selectedPage = document.getElementById(`page${pageNum}`);
    if (selectedPage) {
        selectedPage.style.display = 'block';
    }
}