import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// createRouter 创建路由实例，===> new VueRouter()
// history 是路由模式，hash模式，history模式
// createWebHistory() 是开启history模块 
// createWebHashHistory() 是开启hash模式   

const routes = [
  {
    path: '/',
    name: 'main',
    component: () => import('../views/index.vue')
  },
  {
    path: '/Home',
    name: 'home',
    component: () => import('../views/Home/index.vue')
  },
  {
    path: '/LogIn',
    name: 'login',
    component: () => import('../views/LogIn/index.vue')
  },

] as RouteRecordRaw[]
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router