<template>
  <div class="page-wrapper">
    <div>
      <NavBar></NavBar>
    </div>
    <div class="page-content">
      <articleCard></articleCard>
    </div>
    <!-- 这里可以加其他内容 -->
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/layout/nav-bar/index.vue'
import articleCard from './components/article-card.vue';
</script>

<style lang="scss">
.page-wrapper {
  max-width: 60%;
  margin: 0 auto;
  width: 100%;
}

.page-content {
  padding: 0 20px;
}
</style>