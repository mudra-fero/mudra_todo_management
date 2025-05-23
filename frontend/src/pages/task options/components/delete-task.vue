<script>
import { ref, watch } from 'vue'
import { taskServices } from '@/services/tasks'
import { toastUtility } from '@/utilities/toast-utility'

export default {
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    taskId: {
      type: Number,
      required: true
    }
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      isOpen: this.modelValue
    }
  },
  watch: {
    modelValue(val) {
      this.isOpen = val
    },
    isOpen(val) {
      this.$emit('update:modelValue', val)
    }
  },
  methods: {
    cancelDelete() {
      this.$emit('update:modelValue', false)
    },
    async confirmDelete() {
      try {
        await taskServices.deleteTask(this.taskId)
        toastUtility.showSuccess('Task deleted successfully')
        this.$emit('submit')
        this.$emit('update:modelValue', false)
      } catch (error) {
        toastUtility.showError('Failed to delete task')
      }
    }
  }
}
</script>

<template>
  <v-dialog v-model="isOpen" max-width="500px">
    <v-card style="background-color: #F5F3EF">
      <v-card-title class="text-h5 d-flex justify-center">
        Are you sure you want to delete?
      </v-card-title>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="5">
            <v-btn color="#3E4E3C" block @click="confirmDelete">
              Delete
            </v-btn>
          </v-col>
          <v-col cols="5">
            <v-btn color="grey" block @click="cancelDelete">
              Cancel
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
