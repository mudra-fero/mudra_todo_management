import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: () => import('@/pages/register.vue'),
    },
    {
      path: '/',
      name: 'login',
      component: () => import('@/pages/login.vue'),
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/pages/users/index.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    return next('/')
  }
  if ((to.path === '/' || to.path === '/register') && token) {
    return next('/users')
  }
  next()
})

export default router
