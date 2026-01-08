import AppLayout from "@/layout/AppLayout.vue";
import type { RouteRecordRaw } from "vue-router";




export const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: 'test',
                component: ()=> import('@/views/t1t/test.vue')
            },
                {
                path: 'home',
                component: ()=> import('@/views/home-page/index.vue')
            },
        ]
    }
]