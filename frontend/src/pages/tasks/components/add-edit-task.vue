<script setup>
import { ref, reactive, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from '@vuelidate/validators'
import { toastUtility } from '@/utilities/toast-utility'
import { taskLifecycleStatusChoices, taskPriorityChoices } from '@/utilities/choice-filter-utility'
import { computed } from 'vue'
import { taskServices } from '@/services/tasks'

const props = defineProps({
  modelValue: Boolean,
  editTask: Object,
})
const isEditMode = computed(() => !!props.editTask)
const emit = defineEmits(['update:modelValue', 'submit', 'close'])
const isOpen = ref(props.modelValue)

const taskForm = reactive({
  title: '',
  description: '',
  priority: '',
  lifecycle: '',
  deadline: new Date(),
})

const showError = ref(false)

const rules = {
  title: { required: helpers.withMessage('Title is required', required) },
  description: { required: helpers.withMessage('description is required', required) },
  priority: { required: helpers.withMessage('priority is required', required) },
  deadline: { required: helpers.withMessage('deadline is required', required) },
  lifecycle: { required: helpers.withMessage('lifecycle is required', required) }
}

watch(() => props.modelValue, (val) => {
  isOpen.value = val
})

watch(isOpen, (val) => {
  emit('update:modelValue', val)
})

function resetForm() {
  taskForm.title = ''
  taskForm.description = ''
  taskForm.priority = ''
  taskForm.deadline = ''
  showError.value = false
  v$.value.$reset()
}

const v$ = useVuelidate(rules, taskForm)


watch(() => props.editTask, (val) => {
  if (val) {
    taskForm.title = val.title
    taskForm.description = val.description
    taskForm.priority = String(val.priority)
    taskForm.lifecycle = String(val.lifecycle_stage)
    taskForm.deadline = new Date(val.deadline)
  } else {
    resetForm()
  }
})

const handleInviteSubmit = async () => {
    const isValid = await v$.value.$validate()
  if (!isValid) {
    showError.value = true
    return
  }
  try {
    const payload = {
      title: taskForm.title,
      description: taskForm.description,
      priority: taskForm.priority,
      lifecycle_stage: taskForm.lifecycle,
      deadline: taskForm.deadline?.toISOString().split('T')[0],
    }

    if (isEditMode.value) {
      await taskServices.updateTask(props.editTask.id, payload)
      toastUtility.showSuccess('Task updated successfully.')
    } else {
      await taskServices.addTask(payload)
      toastUtility.showSuccess('Task added successfully.')
    }

    emit('submit')
    emit('update:modelValue', false)
    resetForm()

  } catch (error) {
    toastUtility.showError(error)
  }
}


function formCancel() {
  resetForm()
  emit('update:modelValue', false)
}
</script>

<template>
  <v-dialog v-model="isOpen" persistent max-width="500px">
    <v-card style="background-color: #F5F3EF">
      <v-card-title class="text-h5 d-flex justify-center">Fill task details</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form @submit.prevent="handleInviteSubmit">
          <v-label class="mb-1">Title</v-label>
          <v-text-field v-model="taskForm.title" placeholder="Enter title" :error="v$.title.$error"
            :error-messages="v$.title.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Description</v-label>
          <v-textarea v-model="taskForm.description" placeholder="Enter description" :error="v$.description.$error"
            :error-messages="v$.description.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Priority</v-label>
          <v-select v-model="taskForm.priority" :items="taskPriorityChoices" item-title="value" item-value="key"
            variant="outlined" :error="v$.priority.$error" :error-messages="v$.priority.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Lifecycle status</v-label>
          <v-select v-model="taskForm.lifecycle" :items="taskLifecycleStatusChoices" item-title="value" item-value="key"
            variant="outlined" :error="v$.lifecycle.$error"
            :error-messages="v$.lifecycle.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Deadline</v-label>
          <VueDatePicker v-model="taskForm.deadline" variant="outlined" :error="v$.deadline.$error"
            :error-messages="v$.deadline.$errors.map(e => e.$message)" placeholder="Deadline"
            :enable-time-picker="false" />

          <v-divider class="mt-3"></v-divider>
          <v-row class="mt-3">
            <v-col col="auto">
              <v-btn type="submit" color="#3E4E3C" block>
                {{ isEditMode ? 'Update' : 'Add' }}
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
