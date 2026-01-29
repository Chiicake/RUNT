import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import ModelTraining from '../views/ModelTraining.vue'
import SimulationDemo from '../views/SimulationDemo.vue'
import TrainingData from '../views/TrainingData.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/model-training',
      name: 'model-training',
      component: ModelTraining,
      meta: { requiresAuth: true }
    },
    {
      path: '/simulation-demo',
      name: 'simulation-demo',
      component: SimulationDemo,
      meta: { requiresAuth: true }
    },
    {
      path: '/training-data/:id',
      name: 'training-data',
      component: TrainingData,
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫，检查登录状态
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 这个路由需要授权，请检查是否已登录
    if (!isLoggedIn) {
      // 未登录，重定向到登录页面
      next({ name: 'login' })
    } else {
      // 已登录，继续
      next()
    }
  } else {
    // 不需要授权的路由，继续
    next()
  }
})

export default router