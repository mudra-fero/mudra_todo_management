<script setup>
import { ref, onMounted } from 'vue'
import { userServices } from '@/services/users'
import { userRoleChoices } from '@/utilities/choice-filter-utility'
const props = defineProps({
  rail: Boolean
})
const emit = defineEmits(['update:rail'])
const currentUserRole = ref('')
onMounted(async () => {
  const response = await userServices.getCurrentUser()
  currentUserRole.value = userRoleChoices.find(c => c.key === response.data[0].role)?.value
})

const isAllowed = (allowedRoles) => {
  return allowedRoles.includes(currentUserRole.value)
}
</script>

<template>
  <v-navigation-drawer app permanent :rail="rail" expand-on-hover color="#3E4E3C">
    <v-list dense nav>
      <v-list-item prepend-icon="mdi-view-dashboard" title="Tasks" :to="{ name: 'tasks' }" link />
      <v-list-item v-if="isAllowed(['Admin'])" prepend-icon="mdi-account" title="Users" :to="{ name: 'users' }" link />
      <v-list-item prepend-icon="mdi-file-tree" title="Tasks (Options Api)" :to="{ name: 'tasksOptions' }" link />
    </v-list>
  </v-navigation-drawer>
</template>
