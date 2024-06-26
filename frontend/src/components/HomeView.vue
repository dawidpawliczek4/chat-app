<script setup lang="ts">
import { useWebSocket } from '@vueuse/core'
import axios from 'axios';
import { ref } from 'vue';

interface Message {
  sender: string
  content: string
  timestamp: string
}

const serverId = '1'
const channelId = '1'

const downloadMessageHistory = async () => {
  const response = await axios.get(`http://localhost:8000/api/messages/?channel_id=${channelId}`)
  const data = await response.data
  messages.value = data
}

const messages = ref<Message[]>([])
const messageToSend = ref('')
const socketUrl = `ws://localhost:8000/${serverId}/${channelId}`;
const { send } = useWebSocket(socketUrl, {
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
  onError: (err) => {
    console.log('error', err)
  },
  onDisconnected: () => {
    console.log('disconnected')
  },
})

const sendMessage = () => {
  if (messageToSend.value) {
    // send({ message: messageToSend.value })
    send(JSON.stringify({ message: messageToSend.value }))
    messageToSend.value = ''
  }
}

</script>

<template>
  <div>
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

<style scoped></style>
