<template>
  <div class="unauthorized-page">
    <v-container class="fill-height d-flex flex-column justify-center align-center text-center">
      <v-icon size="100" color="#3E4E3C">mdi-alert-circle-outline</v-icon>
      <h1 class="text-h4 mt-4">403 - Unauthorized</h1>
      <p class="mt-2">You don't have permission to access this page.</p>
      <v-btn color="#3E4E3C" class="mt-4" @click="goHome">
        Go to Task
      </v-btn>
    </v-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goHome = () => {
  router.push('/tasks')
}
</script>

<style scoped>
.unauthorized-page {
  background-color: #F5F3EF;
  color: #3E4E3C !important;
  min-height: 100vh;
}
</style>
