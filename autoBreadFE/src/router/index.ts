import { createRouter, createWebHistory } from 'vue-router'
import { constantRoute } from './routes'
// 创建路由器
const router = createRouter({
  // 路由模式
  history: createWebHistory(),
  routes: constantRoute,
  // 滚动行为
  scrollBehavior() {
    return {
      left: 0, // 水平0
      top: 0, // top0
    }
  },
})

export default router
