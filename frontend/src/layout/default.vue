<script setup>
import { ref } from 'vue'
import Header from '@/shared/Header.vue'
import Sidebar from '@/shared/Sidebar.vue'
const drawer = ref(true)
</script>

<template>
    <v-app>
        <v-main>
            <Header @toggle-drawer="drawer = !drawer" />
            <Sidebar :drawer="drawer" @update:drawer="drawer = $event" />
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