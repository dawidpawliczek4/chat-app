<script setup lang="ts">
import { ref } from 'vue';
import { register } from "../lib/authServices"

const username = ref('');
const password = ref('');

const handleRegister = async (e: Event) => {
    e.preventDefault();
    if (!username.value || !password.value ) {
        alert('Please fill in all fields');
        return;
    }
    register(username.value, password.value); 
}
</script>

<template>
    <div>
        <form @submit="handleRegister">
            <input type="text" placeholder="Username" v-model="username" />
            <input type="password" placeholder="Password" v-model="password" />            
            <button type="submit">Register</button>
        </form>
    </div>
</template>