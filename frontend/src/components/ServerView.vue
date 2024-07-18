<script setup lang="ts">
import axios from 'axios';
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { Channel } from '../types/types';
import AddChannelModal from './AddChannelModal.vue';

const channels = ref<Channel[]>([])

const route = useRoute();
const serverId = computed(() => route.params.serverId as string)
const channelId = computed(() => route.params.channelId as string)

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
    <div class="flex flex-row justify-start items-start ">
        <div class="flex flex-col  p-4 h-screen bg-secondaryBar w-44">
            <p class="font-light text-xs text-gray-300 pb-2">Channels</p>
            <ul class="flex flex-col">
                <router-link :to="`/${serverId}/${channel.id}`" v-for="channel in channels"
                    class="px-2 py-1 rounded-full" :key="channel.id" active-class="bg-black/20"><span
                        class="font-light text-xs text-gray-300">#</span> {{
                            channel.name }}</router-link>
            </ul>

            <AddChannelModal :serverId="serverId" />
        </div>
        <div class="flex grow p-2 h-screen">
            <router-view v-if="channelId" />
            <div v-else class="flex items-center justify-center w-full h-full">
                <p>Pick a channel from the list.</p>
            </div>
        </div>
    </div>
</template>