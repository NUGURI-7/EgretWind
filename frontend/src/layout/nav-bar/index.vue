<template>
  <div class="navbar">
    我是导航栏
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
$navbar-bg: rgb(245, 247, 249);
$navbar-text: #16151a;

.navbar {
  background-color: $navbar-bg;
  color: $navbar-text;
  padding: 16px 20px;
  height: 60px;
  display: flex;
  align-items: center;
}
</style>