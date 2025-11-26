<template>
  <div class="navbar">
    <div class="navbar-content">
      我是导航栏
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
$navbar-bg: rgb(245, 247, 249);
$navbar-text: #16151a;

.navbar {
  width: 100%;
  background-color: $navbar-bg;
  color: $navbar-text;
  box-sizing: border-box;
}

.navbar-content {
  margin: 0 auto;
  padding: 16px 20px;
  height: 60px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
}
</style>