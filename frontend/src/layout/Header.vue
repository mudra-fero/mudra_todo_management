<script setup>
defineEmits(['toggle-drawer'])
</script>

<template>
    <v-app-bar app color="#3E4E3C">
      <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
      <v-toolbar-title></v-toolbar-title>
    </v-app-bar>
  </template>
  