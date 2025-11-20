<template>
    <div class="not-found-container">
        <div>
            <img src="@/assets/404.png" width="250" alt="" />
            <h4 class="text-center">Test</h4>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style lang="scss" scoped>
.not-found-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
}

.text-center {
    text-align: center;
}
</style>