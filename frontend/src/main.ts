import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'
import Components from '@/components'



const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(Components)

app.mount('#app')
