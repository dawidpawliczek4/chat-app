<script lang="ts" setup>
import { ref } from 'vue'
import { FwbButton, FwbModal, FwbInput, FwbSelect } from 'flowbite-vue'
import { useAxiosWithInterceptor } from '../lib/jwtInterceptor';
import { useRouter } from 'vue-router';
import { FwbFileInput } from 'flowbite-vue'

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
const image = ref<File | null>(null)

async function createServer() {

    if (!name.value || !description.value || !category.value) {
        alert('Please fill all fields');
        return;
    }

    if (image.value && !['image/jpeg', 'image/png', 'image/gif'].includes(image.value.type)) {
        alert('Invalid image type');
        return;
    }

    // check if image is under 100x100px
    if (image.value) {
        const img = new Image();
        img.src = URL.createObjectURL(image.value);
        await new Promise(resolve => img.onload = resolve);
        if (img.width > 100 || img.height > 100) {
            alert('Image must be max 100x100px');
            return;
        }
    }

    const formData = new FormData();
    formData.append('name', name.value);
    formData.append('description', description.value);
    formData.append('category', category.value);
    if (image.value) {
        formData.append('icon', image.value);
    }

    try {
        const axiosInstance = useAxiosWithInterceptor();
        await axiosInstance.post('http://localhost:8000/api/server/add/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        router.go(0);

    } catch (error) {
        alert('Error creating server: ' + error);
        console.error(error);
    } finally {
        isShowModal.value = false;
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
                <fwb-file-input v-model="image" label="Server image">
                    <p class="text-sm text-gray-300 mt-1">JPG, JPEG, PNG or GIF (MAX. 100x100px)</p>
                </fwb-file-input>
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