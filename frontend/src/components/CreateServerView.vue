<script setup lang="ts">
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';

const addServer = async () => {
    try {
        const axiosInstance = useAxiosWithInterceptor();
        const response = await axiosInstance.post('http://localhost:8000/api/server/select/', {
            name: 'Test server',
            description: "This is a test server",
            category: "1",
        });

    } catch (error) {
        console.log(error);
        alert("Error: " + error)
    }
}
</script>

<template>
    <div>
        <button @click="addServer">Add test server</button>
    </div>
</template>