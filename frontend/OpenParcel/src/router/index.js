import { createRouter, createWebHistory } from 'vue-router';
import login from '../pages/Login.vue';
import dashboard from '../pages/Dashboard.vue';

const routes = [
  { path: '/login', name: 'Login', component: login },
  { path: '/dashboard', name: 'Dashboard', component: dashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;