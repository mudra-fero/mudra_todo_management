<script setup>
import { ref, onMounted } from 'vue'
import { authenticationService } from '@/services/authentication';
import { toastUtility } from '@/utilities/toast-utility';
import { userServices } from '@/services/users';

defineEmits(['toggle-drawer'])

const username = ref('');
const role = ref('');

const fetchUser = async () => {
  try {
    const response = await userServices.getCurrentUser();
    username.value = response.data[0].username;
    role.value = response.data[0].role;
  } catch (error) {
    toastUtility.showError(error);
  }
};

onMounted(() => {
  fetchUser();
});

</script>

<template>
  <v-app-bar app color="#3E4E3C">
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title>Task Managment</v-toolbar-title>
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-icon icon="mdi-account-circle" size="x-large" v-bind="props" class="mr-5"></v-icon>
      </template>

      <v-card min-width="240">
        <v-list>
          <v-list-item prepend-avatar="src/assets/user.png" :subtitle="role" :title="username">
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-list-item>
            <v-btn variant="text"> Profile </v-btn>
          </v-list-item>

          <v-list-item>
            <v-btn variant="text" @click="authenticationService.logout()"> Logout </v-btn>
          </v-list-item>
        </v-list>
      </v-card>

    </v-menu>
  </v-app-bar>
</template>