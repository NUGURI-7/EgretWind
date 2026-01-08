import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Components from '@/components'
import Aura from '@primeuix/themes/aura';
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import PrimeVue from 'primevue/config';
// main.ts
console.log('开始导入 CSS')
import './styles/main.css'
console.log('CSS 导入完成')

// 检查文件是否真的存在
fetch('/src/styles/main.css')
  .then(res => {
    console.log('CSS 文件状态:', res.status)
    return res.text()
  })
  .then(text => {
    console.log('CSS 文件内容长度:', text.length)
  })
  .catch(err => {
    console.error('CSS 文件加载失败:', err)
  })



const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Components)
app.use(ToastService)
app.use(ConfirmationService)

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.mount('#app')
