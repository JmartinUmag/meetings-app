import { RouteRecordRaw } from 'vue-router'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import ListUsers from '@/views/ListUsers.vue'

const routes: RouteRecordRaw[] = [
  { name: 'Login', path: '/login', component: Login },
  { name: 'Home', path: '/', component: Home, meta: { requiresAuth: true } },
  {
    name: 'ListUsers',
    path: '/users/',
    component: ListUsers,
    meta: { requiresAuth: true },
  },
]

export default routes
