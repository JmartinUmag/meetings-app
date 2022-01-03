import { RouteRecordRaw } from 'vue-router'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import ListUsers from '@/views/ListUsers.vue'
import NewMeeting from '@/views/NewMeeting.vue'
import ViewMeeting from '@/views/ViewMeeting.vue'

const routes: RouteRecordRaw[] = [
  { name: 'Login', path: '/login', component: Login },
  { name: 'Home', path: '/', component: Home, meta: { requiresAuth: true } },
  {
    name: 'ListUsers',
    path: '/users/',
    component: ListUsers,
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    name: 'NewMeeting',
    path: '/meetings/new',
    component: NewMeeting,
    meta: { requiresAuth: true },
  },
  {
    name: 'ViewMeeting',
    path: '/meetings/:id',
    component: ViewMeeting,
    meta: { requiresAuth: true },
  },
]

export default routes
