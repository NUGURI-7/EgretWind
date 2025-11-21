import type { RouteRecordRaw } from "vue-router";




export const routes: Array<RouteRecordRaw> = [
    {
        path: '/test',
        component: ()=> import('@/views/t1t/test.vue')
    },
    {
        path: '/tiptap',
        component: ()=> import('@/views/tiptap/tiptap.vue')
    },
    {
        path: '/el_tap',
        component: ()=> import('@/views/el-tap/el-tap.vue')
    },
]