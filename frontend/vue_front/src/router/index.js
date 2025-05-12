import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomePage.vue'), meta: { public: true } },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginPage.vue'), meta: { public: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterPage.vue'), meta: { public: true } },
  { path: '/about', name: 'About', component: () => import('@/views/AboutPage.vue'), meta: { public: true } },
  { path: '/privacy', name: 'Privacy', component: () => import('@/views/PrivacyPage.vue'), meta: { public: true } },
  { path: '/terms', name: 'Terms', component: () => import('@/views/TermsPage.vue'), meta: { public: true } },
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/DashboardPage.vue') },
  { path: '/food', name: 'Food', component: () => import('@/views/FoodPage.vue') },
  { path: '/exercise', name: 'Exercise', component: () => import('@/views/ExercisePage.vue') },
  { path: '/reports', name: 'Reports', component: () => import('@/views/ReportsPage.vue') }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = false
  
  try {
    await axios.get('/api/users/me/')
    isLoggedIn = true
  }
  catch (error) {
    isLoggedIn = false
  }

  if (to.meta.public) {
    if (to.name === 'Home' && isLoggedIn) {
      next('/dashboard')
    } 
    else {
      next()
    }
  } 
  else {
    if (!isLoggedIn) {
      next('/login')
    } 
    else {
      next()
    }
  }
})

export default router
