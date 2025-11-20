import type { RouteRecordRaw } from "vue-router";




export const routes: Array<RouteRecordRaw> = [
    {
        path: '/test',
        component: ()=> import('@/views/t1t/test.vue')
    },
]