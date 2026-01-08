<template>
  <div class="w-full max-w-3xl md:max-w-4xl lg:max-w-7xl xl:max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
    <div>
      <NavBar></NavBar>
    </div>
    <div class="py-6">
      <articleCard></articleCard>
    </div>
    <!-- 这里可以加其他内容 -->
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/layout/nav-bar/index.vue'
import articleCard from './components/article-card.vue'
</script>
