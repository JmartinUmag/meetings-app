import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import mainRoutes from '@/router/main'
import { useTokenStore } from '@/stores/token'

const routes: Array<RouteRecordRaw> = [
  ...mainRoutes,
  { path: '/:catchAll(.*)', redirect: '/' },
]

const baseUrl = import.meta.env.PROD
  ? String(import.meta.env.VITE_BASE_PATH)
  : '/'
const router = createRouter({
  history: createWebHistory(baseUrl),
  routes,
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useTokenStore()

  if (to.matched.some((route) => route.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' })
    }
  }
  next()
})

export default router
