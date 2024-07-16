<script setup lang="ts">
import { ref } from 'vue';
import { register } from "../lib/authServices"
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const router = useRouter();

const handleRegister = async (e: Event) => {
    e.preventDefault();
    if (!username.value || !password.value) {
        alert('Please fill in all fields');
        return;
    }
    try {
        register(username.value, password.value);
        router.push("/login");
    } catch (error) {
        console.log(error);
        alert("Error: " + error)
    }

}
</script>

<template>
    <div>
        <form @submit="handleRegister">
            <input type="text" placeholder="Username" v-model="username" />
            <input type="password" placeholder="Password" v-model="password" />
            <button type="submit">Register</button>
        </form>
        <p>Or <router-link to="/login">Login</router-link></p>
    </div>
</template>