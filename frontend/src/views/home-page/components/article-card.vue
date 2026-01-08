<template>
  <div>
    <div v-for="article in articles" :key="article.id">
      <Card @click="goToDetail(article.id)" style="margin-bottom: 1rem; cursor: pointer">
        <template #title>
          <h2>{{ article.title }}</h2>
        </template>
        <template #content>
          <p>{{ article.author.username }}</p>
        </template>
      </Card>
    </div>

    <div>
      <Button
        class="outline outline-offset-1 !outline-yellow-300 border-none"
        @click="ss"
        label="sssssssssss"
      />
    </div>

    <div v-if="articles.length === 0" class="empty-state">
      <i class="pi pi-inbox" style="font-size: 3rem; color: #6c757d"></i>
      <p style="color: #6c757d; margin-top: 1rem">暂无文章</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Article } from '@/api/type/article'
import articleApi from '@/api/article'

const router = useRouter()
const articles = ref<Article[]>([])

function getHomeArticleList() {
  articleApi.getArticleList().then((res: any) => {
    articles.value = res.data
  })
}

function goToDetail(id: number) {
  router.push(`/article/${id}`)
}

function ss() {
  getHomeArticleList()
}

onMounted(() => {
  getHomeArticleList()
})
</script>
