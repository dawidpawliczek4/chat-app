<script setup lang="ts">
import { useWebSocket } from '@vueuse/core'
import axios from 'axios';
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { logout, refreshAccessToken } from '../lib/authServices';
import { Message } from '../types/types';
import { useRoute } from 'vue-router';

const route = useRoute();

const messages = ref<Message[]>([])
const messageToSend = ref('')
const messageListRef = ref<HTMLElement | null>(null)

const serverId = ref(route.params.serverId)
const channelId = ref(route.params.channelId)
const access_token = ref(localStorage.getItem('access'))
const refresh_token = ref(localStorage.getItem('refresh'))

const socketUrl = computed(() => `ws://localhost:8000/${serverId.value}/${channelId.value}`)
const messagesUrl = computed(() => `http://localhost:8000/api/messages/?channel_id=${channelId.value}&server_id=${serverId.value}`)

let socket: any;

const createWebSocket = () => {

  socket = useWebSocket(socketUrl.value, {
    autoReconnect: {
      retries: 3,
      delay: 1000,
    },
    onConnected: () => {
      downloadMessageHistory()
      console.log('connected')
    },
    onMessage: (ws: WebSocket, event: MessageEvent) => {
      const data = JSON.parse(event.data)
      const message = {
        sender: data.new_message.sender,
        content: data.new_message.content,
        timestamp: data.new_message.timestamp,
      }

      messages.value = [...messages.value, message]
      scrollListToBottom()
    },
    onError: (ws, event) => {
      console.log('error', event)
    },
    onDisconnected: (ws, event) => {
      console.log("disconnected", event)
      if (event.code === 4001) {
        try {
          refreshAccessToken()
        } catch (error) {
          console.error(error)
          logout()
        }
      }
    },
  })
}

const downloadMessageHistory = async () => {
  const response = await axios.get(messagesUrl.value)
  const data = await response.data
  messages.value = data
  scrollListToBottom()
}

const updateCookies = () => {
  document.cookie = `access_token = ${access_token.value}; path=/`
  document.cookie = `refresh_token = ${refresh_token.value}; path=/`
}

watch(access_token, updateCookies, { immediate: true })
watch(refresh_token, updateCookies, { immediate: true })


// watch(route.params, async (newParams) => {
//   console.log(newParams)
//   serverId.value = newParams.serverId
//   channelId.value = newParams.channelId
//   downloadMessageHistory()
// })

watch(() => route.params, async (newRouteParams) => {
  serverId.value = newRouteParams.serverId
  channelId.value = newRouteParams.channelId

  if (socket && socket.close) {
    socket.close()
  }

  createWebSocket()

  downloadMessageHistory()
})

const sendMessage = () => {
  if (messageToSend.value && socket) {
    // send({ message: messageToSend.value })    
    socket.send(JSON.stringify({ message: messageToSend.value }))
    messageToSend.value = ''
    scrollListToBottom()
  }
}


const scrollListToBottom = () => {
  nextTick(() => {    
    if (messageListRef.value) {
      console.log(messageListRef.value)
      messageListRef.value.lastElementChild?.scrollIntoView()
      
    }
  })
}

const handleStorageChange = (event: StorageEvent) => {
  if (event.key === 'access') {
    access_token.value = localStorage.getItem('access')
  }
  if (event.key === 'refresh') {
    refresh_token.value = localStorage.getItem('refresh')
  }
}

onMounted(() => {
  window.addEventListener('storage', handleStorageChange)
  createWebSocket()
})

</script>

<template>
  <div class="flex flex-col pl-6 py-8 gap-y-2">
    <h1>Messages</h1>
    <div class="flex flex-col h-[360px] overflow-y-auto">
      <ul class="grow" ref="messageListRef">
        <li v-for="message in messages" :key="message.timestamp"
          class="flex flex-col rounded-2xl bg-black/10 px-4 py-1 mt-2">
          <div><strong>{{ message.sender }}</strong></div>
          <p class="font-light">{{ message.content }}</p>
        </li>
      </ul>
    </div>
    <div class="flex gap-x-2">
      <input type="text" v-model="messageToSend" @keyup.enter="sendMessage"
        class="rounded-md bg-secondaryBar border-[1px] focus:outline-1 focus:outline-gray-900  border-white/10 px-3 py-1 text-sm font-light" />
      <button @click="sendMessage">Send</button>
    </div>
  </div>

</template>