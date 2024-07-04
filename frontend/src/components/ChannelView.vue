<script setup lang="ts">
import { useWebSocket } from '@vueuse/core'
import axios from 'axios';
import { ref } from 'vue';
import { store } from '../store/store';
import { logout, refreshAccessToken } from '../lib/authServices';
import { Message } from '../types/types';
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';
import { useRoute } from 'vue-router';

const route = useRoute();

const messages = ref<Message[]>([])
const messageToSend = ref('')
const username = ref('')

const serverId = route.params.serverId
const channelId = route.params.channelId

const downloadMessageHistory = async () => {
  const response = await axios.get(`http://localhost:8000/api/messages/?channel_id=${channelId}`)
  const data = await response.data
  messages.value = data
}

const access_token = localStorage.getItem('access')
const refresh_token = localStorage.getItem('refresh')
document.cookie = `access_token=${access_token}`
document.cookie = `refresh_token=${refresh_token}`

const socketUrl = `ws://localhost:8000/${serverId}/${channelId}`;

const { send } = useWebSocket(socketUrl, {
  autoReconnect: true,
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
  }
}

const getUserDetails = async () => {
  try {
    const axiosWithInterceptor = useAxiosWithInterceptor()
    const userId = localStorage.getItem("userId")
    const token = localStorage.getItem("access")
    const response = await axiosWithInterceptor.get(`http://localhost:8000/api/account/?user_id=${userId}`)
    username.value = response.data.username
  } catch (error) {
    console.error(error)
  }
}

</script>

<template>
  <div>
    <p>Is logged in: {{ store.isAuthenticated }}</p>
    <button @click="getUserDetails">Get username</button>
    <p>Hello, {{ username }}</p>
    <button @click="logout">Logout</button>
    <h1>Messages</h1>
    <ul>
      <li v-for="message in messages" :key="message.timestamp">
        <strong>{{ message.sender }}</strong>: {{ message.content }}
      </li>
    </ul>
  </div>
  <div>
    <input type="text" v-model="messageToSend" @keyup.enter="sendMessage" />
    <button @click="sendMessage">Send</button>
  </div>

</template>