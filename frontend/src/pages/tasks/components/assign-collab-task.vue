<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { userServices } from '@/services/users'
import { taskServices } from '@/services/tasks'
import { toastUtility } from '@/utilities/toast-utility'

const props = defineProps({
    modelValue: Boolean,
    taskObject: Object,
    mode: {
        type: String,
        default: 'assign'
    }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const isOpen = ref(props.modelValue)
const users = ref([])

const assignCollabForm = reactive({
    assigned_to: null,
    collaborated_with: []
})

watch(
    () => props.taskObject,
    (task) => {        
        if (!task) return;

        assignCollabForm.assigned_to = users.value.find(
            (user) => user.id === task?.assigned_to?.user?.id
        ) || null;

        assignCollabForm.collaborated_with = (task?.collaborated_with || [])
            .map(collab => users.value.find(user => user.id === collab.user.id))
            .filter(Boolean); // remove nulls if user not found
    },
    { immediate: true }
)

watch(() => props.modelValue, (val) => isOpen.value = val)
watch(isOpen, (val) => emit('update:modelValue', val))

onMounted(async () => {
    try {
        const res = await userServices.getAllUserList()
        users.value = res.data
    } catch (e) {
        toastUtility.showError('Failed to load users.')
    }
})

function closeDialog() {
    emit('update:modelValue', false)
}

function resetForm() {
    assignCollabForm.assigned_to = ''
    assignCollabForm.collaborated_with = ''
}
function formCancel() {
    resetForm()
    closeDialog()
    emit('update:modelValue', false)
}
async function handleSubmit() {
    console.log(props.taskObject);
    
    try {
        if (props.mode === 'assign') {
            await taskServices.assignTask(props.taskObject.id, {
                "user_id": assignCollabForm.assigned_to.id
            })
            toastUtility.showSuccess('Task Assigned successfully.')
        }
        if (props.mode === 'collab') {
            await taskServices.collaborateTask(props.taskObject.id, {
                "user_ids": assignCollabForm.collaborated_with.map(user => user.id)
            })
            toastUtility.showSuccess('Task collaborated successfully.')
        }
        emit('submit')
        closeDialog()
    } catch (err) {
        toastUtility.showError(err)
    }
}
</script>

<template>
    <v-dialog v-model="isOpen" max-width="550" persistent>
        <v-card style="background-color: #F5F3EF">
            <v-card-title class="text-h5 text-center">
                {{ props.mode === 'assign' ? 'Assign Task' : 'Add Collaborators' }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-form @submit.prevent="handleSubmit">
                    <v-select v-if="props.mode === 'assign'" v-model="assignCollabForm.assigned_to" :items="users"
                        item-title="username" item-value="id" label="Assign To" return-object class="mb-4"
                        variant="outlined" />

                    <v-select v-if="props.mode === 'collab'" v-model="assignCollabForm.collaborated_with" :items="users"
                        item-title="username" item-value="id" label="Collaborators" multiple return-object class="mb-4"
                        variant="outlined" />
                    <v-divider class="mt-3"></v-divider>
                    <v-row class="mt-3">
                        <v-col col="auto">
                            <v-btn type="submit" color="#3E4E3C" block>
                                submit
                            </v-btn>
                        </v-col>
                        <v-col col="auto">
                            <v-btn type="button" color="grey" block @click="formCancel()">
                                Cancel
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>