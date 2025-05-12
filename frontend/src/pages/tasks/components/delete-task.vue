<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean
})
const emit = defineEmits(['update:modelValue', 'submit'])

const isOpen = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  isOpen.value = val
})
watch(isOpen, (val) => {
  emit('update:modelValue', val)
})

function cancelDelete() {
  emit('update:modelValue', false)
}
</script>

<template>
  <v-dialog v-model="isOpen" max-width="500px">
    <v-card style="background-color: #F5F3EF">
      <v-card-title class="text-h5 d-flex justify-center">Are you sure you want to delete?</v-card-title>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="5">
            <v-btn type="button" color="#3E4E3C" block @click="$emit('submit')">
              Delete
            </v-btn>
          </v-col>
          <v-col cols="5">
            <v-btn type="button" color="grey" block @click="cancelDelete">
              Cancel
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
