<script setup>
const props = defineProps({
  drawer: Boolean,
})
const emit = defineEmits(['update:drawer'])
</script>

<template>
    <v-navigation-drawer
      app
      :model-value="drawer"
      @update:model-value="$emit('update:drawer', $event)"
      color="#A8BBA2"
    >
      <v-list dense>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" value="dashboard"></v-list-item>
        <v-list-item prepend-icon="mdi-account" title="Users" :to="{ name: 'users' }" link></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </template>
  