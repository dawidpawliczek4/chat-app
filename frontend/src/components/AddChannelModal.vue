<script lang="ts" setup>
import { ref } from 'vue'
import { FwbButton, FwbModal, FwbInput, FwbSelect } from 'flowbite-vue'
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';
import { useRouter } from 'vue-router';

const props = defineProps<{
    serverId: string
}>()

const router = useRouter()

const isShowModal = ref(false)

function closeModal() {
    isShowModal.value = false
}
function showModal() {
    isShowModal.value = true
}

const name = ref('')
const topic = ref('')

async function createChannel() {

    if (!name.value || !topic.value) {
        alert('Please fill all fields');
        return;
    }

    isShowModal.value = false

    try {
        const axiosInstance = useAxiosWithInterceptor();
        await axiosInstance.post('http://localhost:8000/api/server/channel/', {
            name: name.value,
            description: topic.value,
            server: props.serverId
        });

        router.go(0);
        
    } catch (error) {
        alert('Error creating channel: ' + error);
        console.error(error);
    }
}

</script>

<template>
    <fwb-button @click="showModal" class="mt-4">
        Add channel
    </fwb-button>

    <fwb-modal v-if="isShowModal" @close="closeModal" class="dark">
        <template #header>
            <div class="flex items-center text-lg">
                Create a new channel
            </div>
        </template>
        <template #body>
            <div class="flex flex-col gap-y-4">
                <fwb-input v-model="name" label="Channel name" placeholder="Enter channel name" />
                <fwb-input v-model="topic" label="Channel topic" placeholder="Enter channel topic" />
            </div>
        </template>
        <template #footer>
            <div class="flex justify-between">
                <fwb-button @click="closeModal" color="alternative">
                    Cancel
                </fwb-button>
                <fwb-button @click="createChannel" color="green">
                    Create
                </fwb-button>
            </div>
        </template>
    </fwb-modal>
</template>