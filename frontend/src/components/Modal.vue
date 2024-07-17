<script lang="ts" setup>
import { ref } from 'vue'
import { FwbButton, FwbModal, FwbInput, FwbSelect } from 'flowbite-vue'
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';
import { useRouter } from 'vue-router';


const router = useRouter()

const isShowModal = ref(false)

function closeModal() {
    isShowModal.value = false
}
function showModal() {
    isShowModal.value = true
}

const name = ref('')
const description = ref('')
const category = ref('')

async function createServer() {

    if (!name.value || !description.value || !category.value) {
        alert('Please fill all fields');
        return;
    }

    isShowModal.value = false

    try {
        const axiosInstance = useAxiosWithInterceptor();
        await axiosInstance.post('http://localhost:8000/api/server/add/', {
            name: name.value,
            description: description.value,
            category: category.value,
            channel_server: []
        });


    } catch (error) {
        alert('Error creating server: ' + error);
        console.error(error);
    }
}

</script>

<template>
    <fwb-button @click="showModal">
        Add server
    </fwb-button>

    <fwb-modal v-if="isShowModal" @close="closeModal" class="dark">
        <template #header>
            <div class="flex items-center text-lg">
                Create a new server
            </div>
        </template>
        <template #body>
            <div class="flex flex-col gap-y-4">
                <fwb-input v-model="name" label="Server name" placeholder="Enter server name" />
                <fwb-input v-model="description" label="Server description" placeholder="Enter server description" />
                <fwb-select v-model="category" label="Category"
                    :options="[{ name: 'Category 1', value: '1' }, { name: 'Category 2', value: '2' }]" />
            </div>
        </template>
        <template #footer>
            <div class="flex justify-between">
                <fwb-button @click="closeModal" color="alternative">
                    Cancel
                </fwb-button>
                <fwb-button @click="createServer" color="green">
                    Create
                </fwb-button>
            </div>
        </template>
    </fwb-modal>
</template>