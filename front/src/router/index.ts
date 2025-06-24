import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'begin',
    redirect: '/Main'
  },
  {
    path: '/Main',
    name: 'main',
    component: () => import('../views/Home/index.vue')
  },
  {
    path: '/Home',
    name: 'home',
    component: () => import('../views/index.vue')
  },

] as RouteRecordRaw[]
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router