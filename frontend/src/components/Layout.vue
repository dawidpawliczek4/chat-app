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

    if (!access_token) {
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

    const user = parseJwt(access_token);

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

onMounted(async () => {
    userName.value = await getUserName()
})
</script>


<template>
    <div class="flex flex-row justify-start items-start h-screen">
        <nav class="h-screen border-black border-[1px] p-4 px-8 flex flex-col">
            <p>Hello, {{ userName }}</p>
            <button v-if="isLoggedIn" class="border-[1px] rounded-md">Logout</button>
            <button v-else class="border-[1px] rounded-md">Login</button>
            <router-link to="/">Home</router-link>
            <p>Servers: </p>
            <ul>
                <li v-for="server in servers" :key="server.id">
                    <router-link :to="'/' + server.id">{{ server.name }}</router-link>
                </li>
            </ul>
        </nav>
        <main class="">
            <router-view v-if="serverId" />
            <p v-else>Pick a server from the list.</p>
        </main>
    </div>

</template>