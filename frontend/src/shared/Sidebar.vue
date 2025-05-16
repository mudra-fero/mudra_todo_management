<script setup>
import { ref, onMounted } from 'vue'
const props = defineProps({
  rail: Boolean
})
const emit = defineEmits(['update:rail'])
const currentUserRole = ref('')
onMounted(() => {
  const storedRoleKey = localStorage.getItem('user_role').split('"')[1];
  currentUserRole.value = storedRoleKey || ''
})

const isAllowed = (allowedRoles) => {
  return allowedRoles.includes(currentUserRole.value)
}
</script>

<template>
  <v-navigation-drawer
    app
    permanent
    :rail="rail"
    expand-on-hover
    color="#3E4E3C"
  >
    <v-list dense nav>
      <v-list-item
        prepend-icon="mdi-view-dashboard"
        title="Tasks"
        :to="{ name: 'tasks' }"
        link
      />
      <v-list-item
        prepend-icon="mdi-account"
        title="Users"
        :to="{ name: 'users' }"
        link
      />
    </v-list>
  </v-navigation-drawer>
</template>
