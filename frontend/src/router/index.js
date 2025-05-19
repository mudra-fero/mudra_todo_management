import { createRouter, createWebHistory } from 'vue-router'
import { userRoleChoices } from '@/utilities/choice-filter-utility'
import { userServices } from '@/services/users'
import { localStorageUtility } from '@/utilities/local-storage-utility'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: () => import('@/pages/register.vue'),
      meta: { title: 'Register' }
    },
    {
      path: '/',
      name: 'login',
      component: () => import('@/pages/login.vue'),
      meta: { title: 'Login' }
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('@/pages/not-authorized.vue'),
      meta: { title: 'Unauthorized' }
    },
    {
      path: '/',
      component: () => import('@/layout/default.vue'),
      children: [
        {
          path: '/users',
          name: 'users',
          component: () => import('@/pages/users/index.vue'),
          meta: {
            requiresAuth: true, title: 'User managment', role: [
              "Admin",
            ]
          },
        },
        {
          path: '/tasks',
          name: 'tasks',
          component: () => import('@/pages/tasks/index.vue'),
          meta: { requiresAuth: true, title: 'Task managment' },
        },
        {
          path: '/tasks/:id',
          name: 'TaskDetail',
          component: () => import('@/pages/tasks/TaskDetail.vue'),
          meta: { requiresAuth: true, title: 'Task details' },
        },

      ]
    },

  ],
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    return next('/')
  }
  if ((to.path === '/' || to.path === '/register') && token) {
    return next('/tasks')
  }
  if (token) {
    const response = await userServices.getCurrentUser()
    const user_role = userRoleChoices.find(c => c.key === response.data[0].role)?.value
    if (to.meta.role && !to.meta.role.includes(user_role)) {
      return next('/unauthorized')
    }
  }
  next()
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
