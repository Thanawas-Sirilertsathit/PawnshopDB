import { createRouter, createWebHistory } from 'vue-router';
import PawnshopList from '@/views/PawnshopList.vue';

// Just like  urls.py
const routes = [
    {
        path: '/',
        name: 'PawnshopIndexPage',
        component: PawnshopList,
    },
];
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
