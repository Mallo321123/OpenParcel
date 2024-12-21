import { createRouter, createWebHistory } from 'vue-router';
import Login from '../pages/Login.vue';  // Login-Seite importieren
import Dashboard from '../pages/Dashboard.vue';  // Dashboard-Seite importieren

// Definiere die Routen
const routes = [
  {
    path: '/',
    redirect: '/dashboard'  // Umleitung zur Login-Seite
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('token'); // Überprüfe, ob ein Token im LocalStorage vorhanden ist
        if (token) {
          next('/dashboard');
        } else {
          next();
        }
      }
  
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('token');  // Überprüfe, ob der Token vorhanden ist
        if (token) {
          next();
        } else {
          next('/login');
        }
      }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
