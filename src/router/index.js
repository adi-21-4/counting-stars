import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // -----------------------------------------
  // PUBLIC
  // -----------------------------------------

  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
  },

  {
    path: '/members',
    name: 'members',
    component: () => import('../views/Members.vue')
  },

  {
    path: '/wars',
    name: 'wars',
    component: () => import('../views/Wars.vue')
  },

  {
    path: '/stats',
    name: 'stats',
    component: () => import('../views/Stats.vue')
  },

  {
    path: '/join',
    name: 'recruitment',
    component: () => import('../views/Recruitment.vue')
  },


  // -----------------------------------------
  // ADMIN
  // -----------------------------------------

  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('../views/admin/AdminLogin.vue')
  },

  {
    path: '/admin/register',
    name: 'admin-register',
    component: () => import('../views/admin/AdminRegister.vue')
  },

  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: {
      requiresAuth: true
    }
  },

  {
   path: '/admin/requests',
    name: 'admin-requests',
    component: () => import('../views/admin/AdminRequests.vue'),
    meta: {
      requiresAuth: true
    }
  },

  {
    path: '/admin/applications',
    name: 'admin-applications',
    component: () => import('../views/admin/Applications.vue'),
    meta: {
      requiresAuth: true
    }
  },

  {
  path: '/admin/settings',
  name: 'admin-settings',
  component: () => import('../views/admin/ClanSettings.vue'),
  meta: {
    requiresAuth: true
  }
},

  {
    path: '/admin/announcements',
    name: 'admin-announcements',
    component: () => import('../views/admin/Announcements.vue'),
    meta: {
      requiresAuth: true
    }
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})


// -----------------------------------------
// AUTHENTICATION GUARD
// -----------------------------------------

router.beforeEach((to) => {

  const token = localStorage.getItem('admin_token')

  // Trying to access protected admin page
  if (to.meta.requiresAuth && !token) {
    return {
      name: 'admin-login'
    }
  }

  // Already logged in → don't show login page again
  if (
    to.name === 'admin-login' &&
    token
  ) {
    return {
      name: 'admin-dashboard'
    }
  }

  return true
})


export default router