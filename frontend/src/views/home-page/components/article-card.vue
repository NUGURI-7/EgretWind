<template>
    <div class="article-container">
        <!-- 标题 -->
        <div class="section-title">
            <h1>最新文章</h1>
        </div>

        <!-- 文章列表 -->
        <div class="article-list">
            <div v-for="(article, index) in articles" :key="article.id" class="article-item">
                <el-card class="article-card">
                    <div class="article-content">
                        <!-- 左侧：缩略图 -->
                        <div class="article-image">
                            <img :src="article.thumbnail" :alt="article.title" />
                        </div>

                        <!-- 右侧：内容 -->
                        <div class="article-info">
                            <!-- 标题 -->
                            <h2 class="article-title">{{ article.title }}</h2>

                            <!-- 元数据 -->
                            <div class="article-meta">
                                <span class="meta-item">{{ formatDate(article.publishDate) }}</span>
                                <span class="meta-divider">|</span>
                                <span class="meta-item">{{ article.author }}</span>
                                <span class="meta-divider">|</span>
                                <span class="meta-item">
                                    <el-icon>
                                        <ChatDotRound />
                                    </el-icon>
                                    {{ article.commentCount }}
                                </span>
                            </div>

                            <!-- 摘要 -->
                            <p class="article-excerpt">{{ article.excerpt }}</p>

                            <!-- 阅读按钮 -->
                            <div class="article-action">
                                <el-button type="primary" text>阅读全文 ></el-button>
                            </div>
                        </div>
                    </div>
                </el-card>

                <!-- 分割线（最后一项不显示） -->
                <el-divider v-if="index < articles.length - 1" />
            </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper">
            <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :page-sizes="[10, 20, 30, 40]"
                :total="total" layout="prev, pager, next" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChatDotRound } from '@element-plus/icons-vue'

interface Article {
    id: number
    title: string
    thumbnail: string
    author: string
    publishDate: string
    commentCount: number
    excerpt: string
}

// Mock 数据
const mockArticles: Article[] = [
    {
        id: 1,
        title: '关于 Vue 3 Composition API 的深入探讨',
        thumbnail: 'https://via.placeholder.com/200x150?text=Article+1',
        author: 'Nuguri',
        publishDate: '2025-01-15',
        commentCount: 12,
        excerpt: 'Vue 3 的 Composition API 提供了一种更灵活的代码组织方式。相比传统的 Options API，它能更好地处理复杂的逻辑复用，特别是在大型项目中...',
    },
    {
        id: 2,
        title: 'Django REST Framework 最佳实践指南',
        thumbnail: 'https://via.placeholder.com/200x150?text=Article+2',
        author: 'Nuguri',
        publishDate: '2025-01-10',
        commentCount: 5,
        excerpt: '在构建 RESTful API 时，Django REST Framework 提供了强大的功能。本文将深入讨论序列化器、权限管理、缓存策略等核心概念...',
    },
    {
        id: 3,
        title: '数据库索引优化的思考',
        thumbnail: 'https://via.placeholder.com/200x150?text=Article+3',
        author: 'Nuguri',
        publishDate: '2025-01-05',
        commentCount: 0,
        excerpt: '数据库索引是性能优化的关键。我们需要理解不同类型索引的工作原理，以及如何在实际项目中合理应用它们...',
    },
    {
        id: 4,
        title: 'TypeScript 类型系统深度解析',
        thumbnail: 'https://via.placeholder.com/200x150?text=Article+4',
        author: 'Nuguri',
        publishDate: '2024-12-28',
        commentCount: 8,
        excerpt: '理解 TypeScript 的类型系统是写出高质量代码的基础。从基本类型到复杂的泛型，我们逐一探讨...',
    },
    {
        id: 5,
        title: '微服务架构中的分布式事务处理',
        thumbnail: 'https://via.placeholder.com/200x150?text=Article+5',
        author: 'Nuguri',
        publishDate: '2024-12-20',
        commentCount: 15,
        excerpt: '在微服务架构中，分布式事务是一个复杂的问题。Saga 模式、TCC 等多种解决方案各有优劣...',
    },
]

// 状态
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(mockArticles.length)
const articles = ref(mockArticles)

// 工具函数
const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN')
}
</script>

<style lang="scss" scoped>
.article-container {
    padding: 40px 0;
}

.section-title {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #f0f0f0;

    h1 {
        font-size: 28px;
        font-weight: 600;
        color: #16151a;
        margin: 0;
    }
}

.article-list {
    margin-bottom: 40px;
}

.article-item {
    &:not(:last-child) {
        margin-bottom: 20px;
    }
}

.article-card {
    border: 1px solid #f0f0f0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border-radius: 4px;

    :deep(.el-card__body) {
        padding: 20px;
    }
}

.article-content {
    display: flex;
    gap: 30px;
}

.article-image {
    flex-shrink: 0;
    width: 200px;
    height: 150px;
    overflow: hidden;
    border-radius: 4px;
    background-color: #f5f5f5;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

.article-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.article-title {
    font-size: 20px;
    font-weight: 600;
    color: #16151a;
    margin: 0 0 12px 0;
    line-height: 1.4;

    &:hover {
        color: #409eff;
        cursor: pointer;
    }
}

.article-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    font-size: 13px;
    color: #909399;

    .meta-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .meta-divider {
        color: #d9d9d9;
    }

    :deep(.el-icon) {
        font-size: 14px;
    }
}

.article-excerpt {
    font-size: 14px;
    color: #606266;
    line-height: 1.6;
    margin: 0 0 16px 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
    /* 添加标准属性 */
    overflow: hidden;
}

.article-action {
    display: flex;
    justify-content: flex-start;
}

.pagination-wrapper {
    display: flex;
    justify-content: center;
    padding: 20px 0;
}
</style>