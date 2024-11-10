import { ref } from 'vue';
import apiClient from '@/api';
import { createPostRequest } from './HttpRequest';
import { getCookie, setCookie, deleteCookie } from './CookiesReadWrite.js';
import router from '@/router';

export var isAuth = ref(false);
export var fName = ref('');
export var lName = ref('');
export var email = ref('');
export var pfp = ref('');
export var userId = ref(-1);
export var userName = ref('');

// Simple login method, no OAuth
export async function login(credentials) {
    /**
     * Log user in using username and password.
     * This function returns nothing.
     */
    try {
        const response = await createPostRequest(`auth/login/`, credentials);
        setCookie('backend-token', response.data.access); // Store token
        isAuth.value = true;
        await getUserData(); // Fetch user data after login
        const profileStatus = await apiClient.get(`/profile/`);
        if (!profileStatus.data.has_profile) {
            router.push(
                `/create-profile?next=${router.currentRoute.value.path}`
            );
        }
    } catch (e) {
        console.error('Error on login: ', e);
    }
}

// Check authentication status based on cookie
export async function authStatus() {
    /**
     * Check session authentication status
     * This function does not return anything.
     */
    const token = getCookie('backend-token');
    if (token) {
        try {
            await createPostRequest(`rest-auth/token/verify/`, { token });
            isAuth.value = true;
            getUserData();
        } catch (e) {
            await logout();
        }
    } else {
        await logout();
    }
}

// Logout user from the system
export async function logout() {
    /**
     * Logout user from the system.
     * This function returns nothing.
     */
    // await createPostRequest(`rest-auth/logout/`, {});
    isAuth.value = false;
    fName.value = '';
    lName.value = '';
    email.value = '';
    pfp.value = '';
    userId.value = '';
    userName.value = '';
    deleteCookie('backend-token');
}

// Get user data after login
export async function getUserData() {
    /**
     * Get user data from backend.
     * This function returns nothing.
     */
    try {
        const response = await apiClient.get(`rest-auth/user/`);
        fName.value = response.data.first_name;
        lName.value = response.data.last_name;
        email.value = response.data.email;
        userName.value = response.data.username;
        const profilePic = await apiClient.get(`profile-pic/`);
        pfp.value = profilePic.data.profile_picture_url;
        userId.value = response.data.pk;
    } catch (e) {
        console.error(e);
        await logout();
    }
}
