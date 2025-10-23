import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import { getCurrentUser } from '../services/supabase'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard de autenticação atualizado
router.beforeEach(async (to, from, next) => {
  const session = await getCurrentUser()

  if (to.meta.requiresAuth && !session) {
    next('/login')
  } else if (to.path === '/login' && session) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
