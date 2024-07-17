<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { getUserDetails, getUserIdFromToken } from '../lib/authServices';
import { store } from '../store/store';
import { FwbInput } from 'flowbite-vue';

const router = useRouter();

const username = ref('');
const password = ref('');

const handleLogin = async (e: Event) => {
    e.preventDefault();
    if (!username.value || !password.value) {
        alert('Please fill in all fields');
        return;
    }
    try {
        const response = await axios.post('http://localhost:8000/api/token/', {
            username: username.value,
            password: password.value
        });

        const { access, refresh } = response.data;
        localStorage.setItem('access', access);
        localStorage.setItem('refresh', refresh);
        localStorage.setItem('userId', getUserIdFromToken(access));

        store.setIsAuthenticated(true);

        getUserDetails()

        router.push('/')
    } catch (error) {
        alert('Invalid credentials')
        console.error(error);
    }
}
</script>

<template>
    <div class="flex flex-col w-full justify-center items-center h-screen gap-y-4 dark">
        <form @submit="handleLogin" class="flex flex-col gap-y-2">
            <fwb-input type="text" placeholder="Username" v-model="username" />
            <fwb-input type="password" placeholder="Password" v-model="password" />
            <button type="submit" class=" font-semibold hover:text-gray-300">Login</button>
        </form>
        <p class="font-light text-gray-300 tracking-wide"><span class="text-sm">Or</span> <router-link to="/register"
                class="hover:text-white ">Register</router-link></p>
    </div>
</template>