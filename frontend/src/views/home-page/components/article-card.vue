<template>
  <div class="article-list-container">
    <div class="article-grid">
      <div v-for="article in articles" :key="article.id" class="article-card-wrapper">
        <el-card class="article-card" shadow="hover" @click="goToDetail(article.id)">
          <!-- 文章封面图 - 独立引用 -->
          <div class="article-cover">
            <img :src="getArticleCover(article.id)" :alt="article.title" @error="handleImageError" />
          </div>

          <!-- 文章内容 -->
          <div class="article-body">
            <h2 class="article-title">{{ article.title }}</h2>

            <div class="article-meta">
              <span class="author">
                <i class="el-icon-user"></i>
                {{ article.author.username }}
              </span>
              <span class="date" v-if="article.publishedAt">
                <i class="el-icon-time"></i>
                {{ formatDate(article.publishedAt) }}
              </span>
              <span class="status" :class="article.status">
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </div>

            <p class="article-excerpt">
              {{ getExcerpt(article.content) }}
            </p>

            <div class="article-footer">
              <el-button type="primary" link>
                阅读全文 →
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-wrapper">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <span>加载中...</span>
    </div>

    <!-- 空状态 -->
    <el-empty v-if="!loading && articles.length === 0" description="暂无文章" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'
import type { Article } from '@/api/type/article'
import articleApi from '@/api/article'

const router = useRouter()
const articles = ref<Article[]>([])
const loading = ref(false)

function getHomeArticleList() {
  articleApi.getArticleList(undefined, loading).then((res: any) => {
    articles.value = res.data
  })
}

// 获取文章封面图 - 根据文章ID获取对应图片
function getArticleCover(articleId: number) {
  // 这里根据你的实际图片存储方式来修改
  // 方式1: 如果有统一的图片API
  return `/api/articles/${articleId}/cover`

  // 方式2: 如果图片存在固定目录
  // return `/images/articles/${articleId}.jpg`

  // 方式3: 使用 unsplash 占位图
  // return `https://source.unsplash.com/800x600/?nature,${articleId}`
}

// 格式化日期
function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 获取文章摘要
function getExcerpt(content: string, maxLength: number = 100) {
  if (!content) return '暂无内容'
  const plainText = content.replace(/<[^>]*>/g, '').trim()
  return plainText.length > maxLength
    ? plainText.substring(0, maxLength) + '...'
    : plainText
}

// 图片加载失败处理 - 使用SVG占位图
function handleImageError(e: Event) {
  const target = e.target as HTMLImageElement
  // 使用 data URL 的 SVG 占位图
  target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImciIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPjxzdG9wIG9mZnNldD0iMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNjOGQ4YzQ7c3RvcC1vcGFjaXR5OjEiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojYjhjYmI4O3N0b3Atb3BhY2l0eToxIiAvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNjAwIiBmaWxsPSJ1cmwoI2cpIi8+PGNpcmNsZSBjeD0iMjAwIiBjeT0iMzAwIiByPSI4MCIgZmlsbD0iI2FhYzBhNiIgb3BhY2l0eT0iMC40Ii8+PGNpcmNsZSBjeD0iNjAwIiBjeT0iMjAwIiByPSIxMjAiIGZpbGw9IiNhYWMwYTYiIG9wYWNpdHk9IjAuMyIvPjxjaXJjbGUgY3g9IjQwMCIgY3k9IjQwMCIgcj0iNjAiIGZpbGw9IiNhYWMwYTYiIG9wYWNpdHk9IjAuNSIvPjwvc3ZnPg=='
}

// 跳转到文章详情
function goToDetail(id: number) {
  router.push(`/article/${id}`)
}

onMounted(() => {
  getHomeArticleList()
})
</script>

<style lang="scss" scoped>
.article-list-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}

.article-card-wrapper {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.article-card {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e8e3d8;
  transition: all 0.3s ease;
  background: #ffffff;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(139, 125, 107, 0.12);
    border-color: #9aaf9f;

    .article-cover img {
      transform: scale(1.05);
    }

    .article-title {
      color: #5a7c5e;
    }
  }

  :deep(.el-card__body) {
    padding: 0;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

.article-cover {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: linear-gradient(135deg, #c8d8c4 0%, #b8cbb8 100%);
  flex-shrink: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
}

.article-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.article-title {
  font-size: 20px;
  font-weight: 600;
  color: #3d4a3e;
  margin: 0 0 14px 0;
  line-height: 1.5;
  transition: color 0.3s ease;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 14px;
  font-size: 13px;
  color: #8b7d6b;
  flex-wrap: wrap;

  span {
    display: flex;
    align-items: center;
    gap: 5px;

    i {
      font-size: 14px;
    }
  }

  .status {
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;

    &.published {
      background: #d4e4d7;
      color: #4a6b4e;
    }

    &.draft {
      background: #f0ebe3;
      color: #9a8872;
    }
  }
}

.article-excerpt {
  font-size: 14px;
  line-height: 1.7;
  color: #6b6b6b;
  margin: 0 0 auto 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.article-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 14px;
  margin-top: 14px;
  border-top: 1px solid #f0ebe3;

  .el-button {
    font-size: 14px;
    color: #5a7c5e;
    font-weight: 500;

    &:hover {
      color: #4a6b4e;
    }
  }
}

.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #8b7d6b;
  font-size: 15px;
  gap: 12px;

  .el-icon {
    font-size: 28px;
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .article-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

@media (max-width: 768px) {
  .article-list-container {
    padding: 20px 16px;
  }

  .article-cover {
    height: 180px;
  }

  .article-body {
    padding: 20px;
  }

  .article-title {
    font-size: 18px;
  }

  .article-meta {
    font-size: 12px;
    gap: 12px;
  }

  .article-excerpt {
    font-size: 13px;
  }
}
</style>