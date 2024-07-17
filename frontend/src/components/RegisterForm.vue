<script setup lang="ts">
import { ref } from 'vue';
import { register } from "../lib/authServices"
import { useRouter } from 'vue-router';
import { FwbInput } from 'flowbite-vue';

const username = ref('');
const password = ref('');
const repeatPassword = ref('');
const router = useRouter();

const handleRegister = async (e: Event) => {
    e.preventDefault();

    if (password.value !== repeatPassword.value) {
        alert('Passwords do not match');
        return;
    }

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
        <div class="flex flex-col w-full justify-center items-center h-screen gap-y-4 dark">
            <form @submit="handleRegister" class="flex flex-col gap-y-2">
                <fwb-input type="text" placeholder="Username" v-model="username" />
                <fwb-input type="password" placeholder="Password" v-model="password" />
                <fwb-input type="password" placeholder="Repeat password" v-model="repeatPassword" />
                <button type="submit" class=" font-semibold hover:text-gray-300">Register</button>
            </form>
            <p class="font-light text-gray-300 tracking-wide"><span class="text-sm">Or</span> <router-link to="/login"
                    class="hover:text-white ">Login</router-link></p>
        </div>
    </div>
</template>