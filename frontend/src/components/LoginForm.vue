<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { getUserDetails, getUserIdFromToken } from '../lib/authServices';
import { store } from '../store/store';

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
    <div>
        <form @submit="handleLogin">
            <input type="text" placeholder="Username" v-model="username" />
            <input type="password" placeholder="Password" v-model="password" />
            <button type="submit">Login</button>
        </form>
    </div>
</template>