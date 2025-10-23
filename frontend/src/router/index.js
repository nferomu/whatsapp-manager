import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import NumberDetail from '../views/NumberDetail.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/number/:id', name: 'NumberDetail', component: NumberDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
