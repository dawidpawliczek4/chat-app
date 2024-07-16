<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import { Server } from '../types/types';
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';

const servers = ref<Server[]>([])

const route = useRoute();
const serverId = computed(() => route.params.serverId)

const isLoggedIn = ref(localStorage.getItem('isAuthenticated') === 'true')

const userName = ref('')

const getUserName = async () => {
    const axiosInstance = useAxiosWithInterceptor();
    const access_token = localStorage.getItem('access');
    const refresh_token = localStorage.getItem('refresh');


    let token = access_token

    if (!access_token) {
        token = refresh_token
    }
    if (!token) {
        return 'Anonymous'
    }

    const parseJwt = (token: string) => {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    }

    const user = parseJwt(token);

    try {
        const response = await axiosInstance.get('http://localhost:8000/api/account/?user_id=' + user.user_id)
        return response.data.username
    } catch (error) {
        console.log(error)
        isLoggedIn.value = false
        return 'Anonymous'
    }
}

axios.get('http://localhost:8000/api/server/select/')
    .then(response => {
        servers.value = response.data;
        console.log(response.data)
    })
    .catch(error => {
        console.log(error);
    });

const handleLogout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('isAuthenticated')
    isLoggedIn.value = false
}

onMounted(async () => {
    userName.value = await getUserName()
})
</script>


<template>
    <div class="flex flex-row justify-start items-start h-screen">
        <nav class="h-screen   p-4 px-8 flex flex-col w-44 bg-bar">
            <p>Hello, {{ userName }}</p>
            <button v-if="isLoggedIn" class="border-[1px] rounded-md" @click="handleLogout">Logout</button>
            <button v-else class="border-[1px] rounded-md"><router-link to="/login">Login</router-link></button>

            <router-link to="/" class="py-2 mb-2 border-b-[1px]">Home</router-link>
            <p class="text-gray-300 font-light text-xs py-2">Servers</p>            
            <ul>
                <li v-for="server in servers" :key="server.id">
                    <router-link :to="'/' + server.id" active-class="border-l-[1px] pl-2">{{ server.name }}</router-link>
                </li>
                <!-- <router-link to="/add-server" class="mt-2 border-b">Add Server</router-link> -->
                 
            </ul>
        </nav>
        <main class="w-full h-full">
            <router-view v-if="serverId" />
            <div v-else class="flex justify-center items-center w-full h-full"><h1 class="">Pick a server from the list.</h1></div>
        </main>
    </div>

</template>