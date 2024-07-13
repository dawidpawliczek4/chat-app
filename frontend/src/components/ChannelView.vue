<script setup lang="ts">
import { useWebSocket } from '@vueuse/core'
import axios from 'axios';
import { computed, onMounted, ref, watch } from 'vue';
import { store } from '../store/store';
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

const downloadMessageHistory = async () => {
  const response = await axios.get(messagesUrl.value)
  const data = await response.data
  messages.value = data
}

const updateCookies = () => {
  document.cookie = `access_token = ${access_token.value}; path=/`
  document.cookie = `refresh_token = ${refresh_token.value}; path=/`
}

watch(access_token, updateCookies, { immediate: true })
watch(refresh_token, updateCookies, { immediate: true })


watch(route.params, async (newParams) => {
  serverId.value = newParams.serverId
  channelId.value = newParams.channelId
  downloadMessageHistory()
})


const { send } = useWebSocket(socketUrl.value, {
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

const sendMessage = () => {
  if (messageToSend.value) {
    // send({ message: messageToSend.value })
    send(JSON.stringify({ message: messageToSend.value }))
    messageToSend.value = ''
    scrollListToBottom()
  }
}


const scrollListToBottom = () => {
  const messageList = messageListRef.value
  if (messageList) {
    messageList.scrollTop = messageList.scrollHeight
  }
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
  scrollListToBottom()
  window.addEventListener('storage', handleStorageChange)
})

</script>

<template>
  <div>        
    <h1>Messages</h1>
    <div class="flex flex-col h-[360px] overflow-y-auto">
      <ul class="grow" ref="messageListRef">
        <li v-for="message in messages" :key="message.timestamp" class="">
          <strong>{{ message.sender }}</strong>
          <p>{{ message.content }}</p>
        </li>
      </ul>
    </div>
  </div>
  <div>
    <input type="text" v-model="messageToSend" @keyup.enter="sendMessage" />
    <button @click="sendMessage">Send</button>
  </div>

</template>