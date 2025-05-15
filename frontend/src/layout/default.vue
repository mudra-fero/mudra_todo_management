<script setup>
import { ref } from 'vue'
import Header from '@/shared/Header.vue'
import Sidebar from '@/shared/Sidebar.vue'

const rail = ref(false)
</script>

<template>
  <v-app>
    <Header @toggle-rail="rail = !rail" />
    <Sidebar :rail="rail" />
    <v-main>
      <div class="page-content">
        <RouterView />
      </div>
    </v-main>
  </v-app>
</template>

<style scoped>
.page-color {
    background-color: #F5F3EF;
}
</style>