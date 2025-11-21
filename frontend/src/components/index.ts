import { type App } from "vue"
import Tiptap from '@/components/tiptap/Tiptap.vue'










export default {
    install(app: App) {
        app.component('Tiptap',Tiptap)
    }
}