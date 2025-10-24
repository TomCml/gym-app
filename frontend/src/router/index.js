import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Workouts from '../views/Workouts.vue'
import NewWorkout from '../views/NewWorkout.vue'
import History from '../views/History.vue'
import Profile from '../views/Profile.vue'
import WorkoutEdit from '../views/WorkoutEdit.vue'
import LiveWorkout from '../views/LiveWorkout.vue'
import Stats from '../views/Stats.vue'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/workouts',
    name: 'workouts',
    component: Workouts,
    meta: { requiresAuth: true },
  },
  {
    path: '/new-workout',
    name: 'new-workout',
    component: NewWorkout,
    meta: { requiresAuth: true, transition: 'slide-up' },
  },
  {
    path: '/stats',
    name: 'stats',
    component: Stats,
    meta: { requiresAuth: true },
  },
  {
    path: '/workouts/edit/:id',
    name: 'workout-edit',
    component: WorkoutEdit,
    props: true,
    meta: { requiresAuth: true, transition: 'slide-up' },
  },

  {
    path: '/history',
    name: 'history',
    component: History,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { requiresAuth: true },
  },

  { path: '/', redirect: '/login' },

  {
    path: '/:pathMatch(.*)*',
    redirect: () => {
      const authStore = useAuthStore()
      return authStore.isAuthenticated ? '/home' : '/login'
    },
  },
  {
    path: '/liveworkout',
    name: 'liveworkout',
    component: LiveWorkout,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
