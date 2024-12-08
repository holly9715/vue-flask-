import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import IndexView from '@/views/IndexView.vue'
import { useTokenStore } from '@/stores/mytoken'
import test from '@/views/test.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/testa',
      name:'testa',
      component:test
      //测试页面不能使用懒加载
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/LoginView.vue')
    },
    {
      path:'/register',
      name:'register',
      component:()=>import('@/views/login/register.vue')
    },
    {
      path: '/:xxx(.*)*',
      name: 'ErrorPage',
      component: () => import('@/views/ErrorPage.vue')
    },
    {
      path: '/user_look_index',
      name: 'user_look_index',
      component: () => import('@/views/user_look/AppHp.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'user_home',
          component: () => import('@/views/user_look/user_layout/appMain.vue')
        },
        {
          path: '/ocr_project',
          name: 'ocr_project',
          component: () => import('@/views/user_look/user_project/user_ocr.vue')
        },
        {
          path: '/lpdr_project',
          name: 'lpdr_project',
          component: () => import('@/views/user_look/user_project/user_lpdr.vue')
        },
        {
          path: 'car',
          name: 'user_car',
          component: () => import('@/project/car.vue')
        },
        {
          path: 'cooperate',
          name: 'user_cooperate',
          component: () => import('@/project/cooperate.vue')
        },
        {
          path: 'shareData',
          name: 'user_shareData',
          component: () => import('@/project/shareData.vue')
        },
        {
          path: 'fl',
          name: 'user_fl',
          component: () => import('@/project/fl.vue')
        }
      ]
    },
    {
      path: '/',
      name: '',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home',
          component: IndexView
        },
        {
          path: '/user_menu',
          name: 'user_menu',
          component: () => import('@/views/menu/user_managent.vue')
        },
        {
          path: '/lpdr',
          name: 'lpdr',
          component: () => import('@/project/LPDR.vue')
        },
        {
          path: '/ocr',
          name: 'ocr',
          component: () => import('@/project/OCR.vue')
        }
        ,
          {
          path: '/cooperate',
          name: 'cooperate',
          component: () => import('@/project/cooperate.vue')
        }
        ,
          {
          path: '/fl',
          name: 'fl',
          component: () => import('@/project/fl.vue')
        }
        ,
          {
          path: '/car',
          name: 'car',
          component: () => import('@/project/car.vue')
        }
        ,
          {
          path: '/share',
          name: 'shareData',
          component: () => import('@/project/shareData.vue')
        }

      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some((r) => r.meta?.requiresAuth)) {
    const store = useTokenStore()
    if (!store.token.access_token) {
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router
