<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { authenticationService } from '@/services/authentication';
import { userServices } from '@/services/users'
import { toastUtility } from '@/utilities/toast-utility'
import { userRoleChoices } from '@/utilities/choice-filter-utility'
import { notificationService } from '@/services/notification';

defineEmits(['toggle-rail'])

const username = ref('');
const role = ref('');
const notifications = ref([])
const unreadCount = ref(0)

const fetchUser = async () => {
  try {
    const response = await userServices.getCurrentUser()
    username.value = response.data[0].username
    role.value = userRoleChoices.find(c => c.key === response.data[0].role)?.value
  } catch (error) {
    toastUtility.showError(error);
  }
};

const fetchNotifications = async () => {
  try {
    const res = await notificationService.getNotifications()
    notifications.value = res.data.results || []
    unreadCount.value = res.data.unread_count
  } catch (error) {
    toastUtility.showError(error)
  }
}

const clearNotifications = async () => {
  try {
    await notificationService.clearAllNotifications()
    toastUtility.showSuccess('Notifications cleared')
    await fetchNotifications()
  } catch (error) {
    toastUtility.showError(error)
  }
}

let intervalId
onMounted(() => {
  fetchUser();
  fetchNotifications()
  intervalId = setInterval(fetchNotifications, 300000)
});

onBeforeUnmount(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <v-app-bar app color="#3E4E3C">
    <v-app-bar-nav-icon @click="$emit('toggle-rail')" />
    <v-toolbar-title>Task Managment</v-toolbar-title>

    <v-spacer />

    <v-menu offset-y transition="slide-y-transition">
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props">
          <v-badge :content="unreadCount" class="mr-5" color="green" overlap>
            <v-icon>mdi-bell</v-icon>
          </v-badge>
        </v-btn>
      </template>

      <v-card min-width="310">
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Notifications</span>
          <v-icon v-if="notifications.length" size="25" @click="clearNotifications">mdi-close</v-icon>
        </v-card-title>
        <v-divider />
        <v-list style="max-height: 300px; overflow-y: auto;">
          <v-list-item v-for="(notification, index) in notifications" :key="index" class="py-3 subtitle-bordered"
            :class="{ 'unread-notification': !notification.is_read }">
            <v-list-item-subtitle>
              {{ notification.message }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-list-item v-if="!notifications.length" class="text-center">
            No notifications
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>

    <v-menu>
      <template v-slot:activator="{ props }">
        <v-icon icon="mdi-account-circle" size="x-large" v-bind="props" class="mr-5" />
      </template>

      <v-card min-width="240">
        <v-list>
          <v-list-item prepend-avatar="/src/assets/user.png" :subtitle="role" :title="username" />
        </v-list>
        <v-divider />
        <v-list>
          <v-list-item><v-btn variant="text">Profile</v-btn></v-list-item>
          <v-list-item>
            <v-btn variant="text" @click="authenticationService.logout()">Logout</v-btn>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>


<style scoped>
.unread-notification {
  background-color: #e3f2fd;
}

.subtitle-bordered {
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 4px;
  width: 30vh;
  margin-left: 3%;
}
</style>