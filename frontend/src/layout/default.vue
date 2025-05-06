<script setup>
import { ref } from 'vue'
import Header from '@/shared/Header.vue'
import Sidebar from '@/shared/Sidebar.vue'
const drawer = ref(true)
</script>
<template>
        <Header @toggle-drawer="drawer = !drawer"></Header>
        <Sidebar :drawer="drawer" @update:drawer="drawer = $event" />
        <RouterView />
</template>

<style scoped>
.page-color {
    background-color: #F5F3EF;
    margin-top: 7vh;
}
</style>