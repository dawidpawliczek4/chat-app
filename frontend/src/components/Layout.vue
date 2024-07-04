<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const servers = ref([])

const route = useRoute();
const serverId = computed(() => route.params.serverId)


axios.get('http://localhost:8000/api/server/select/')
    .then(response => {
        servers.value = response.data;
        console.log(response.data)
    })
    .catch(error => {
        console.log(error);
    });

</script>


<template>
    <div class="flex flex-row justify-start items-start">
        <nav class="h-screen border-black border-[1px] p-4 px-8 flex flex-col">
            <router-link to="/">Home</router-link>
            <p>Servers: </p>
            <ul>
                <li v-for="server in servers" :key="server.id">
                    <router-link :to="'/' + server.id">{{ server.name }}</router-link>
                </li>
            </ul>
        </nav>
        <main class="grow">
            <router-view v-if="serverId" />
            <p v-else>Pick a server from the list.</p>
        </main>
    </div>

</template>