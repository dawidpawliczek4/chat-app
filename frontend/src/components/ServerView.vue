<script setup>
import axios from 'axios';
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const channels = ref([])

const route = useRoute();
const serverId = computed(() => route.params.serverId)

watch(serverId, (newServerId) => {
    axios.get('http://localhost:8000/api/server/select/?by_serverid=' + newServerId)
        .then(response => {
            const data = response.data;
            const channel_servers = data[0].channel_server;
            channels.value = channel_servers;      
            console.log(channels.value)      
        })
        .catch(error => {
            console.log(error);
        });
}, { immediate: true })

</script>

<template>
    <div class="flex flex-row justify-start items-start">
        <div class="flex flex-col border-black border-l-0 border-[1px] p-4 h-screen">
            <h1>Channels</h1>
            <ul>
                <router-link :to="`/${serverId}/${channel.id}`" v-for="channel in channels" :key="channel.id">{{ channel.name }}</router-link>
            </ul>
        </div>
        <div class="flex grow p-2">
            <router-view />
        </div>
    </div>
</template>