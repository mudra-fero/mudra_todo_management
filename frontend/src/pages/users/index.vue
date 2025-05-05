<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Header from '@/layout/Header.vue'
import Sidebar from '@/layout/Sidebar.vue'
import { watch } from 'vue'
import InviteUserDialog from './components/invite-user.vue'
import DeleteDialog from './components/delete-user.vue'
import { userServices } from '@/services/users'
import { toastUtility } from '@/utilities/toast-utility'
import { authenticationService } from '@/services/authentication'

const showInviteDialog = ref(false)
const drawer = ref(true)
const itemsPerPage = ref(10)
const serverItems = ref([])
const loading = ref(true)
const totalItems = ref(0)
const searchQuery = ref('')
const showDeleteDialog = ref(false)
const userToDelete = ref(null)
const apiUrl = import.meta.env.VITE_BACKEND_BASE_URL
const editingUser = ref(null)

function editUser(user) {
  editingUser.value = { ...user }
  showInviteDialog.value = true
}

function deleteUser(user) {
  userToDelete.value = user
  showDeleteDialog.value = true
}

watch(searchQuery, () => {
  loadItems({ page: 1, itemsPerPage: itemsPerPage.value })
})

const headers = ref([
  { title: 'S.No', key: 'sn', align: 'center', sortable: false },
  { title: 'Username', key: 'username', align: 'center', sortable: false },
  { title: 'Email', key: 'email', align: 'center', sortable: false },
  { title: 'Role', key: 'role', align: 'center', sortable: false },
  { title: 'Assigned Tasks', key: 'assigned_tasks', align: 'center', sortable: false },
  { title: 'Collaborated Tasks', key: 'collaborated_tasks', align: 'center', sortable: false },
  { title: 'Actions', key: 'actions', align: 'center', sortable: false },
])

const fetchUsers = async (params) => {
  params = {
    ...params,
    search: searchQuery.value,
    page: params.page,
    page_size: itemsPerPage,
  }
  try {
    // loaderUtility.show();
    const response = await userServices.getUserList(params);
    return {
      items: response.data.results,
      total: response.data.count,
    }
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    // loaderUtility.hide();
  }
};

function loadItems({ page, itemsPerPage, sortBy }) {
  loading.value = true
  fetchUsers({ page, itemsPerPage, sortBy }).then(({ items, total }) => {
    serverItems.value = items.map((item, index) => ({
      ...item,
      sn: (page - 1) * itemsPerPage + index + 1,
    }))
    totalItems.value = total
    loading.value = false
  })
}

async function handleInviteSubmit(payload) {
  try {
    if (payload.id) {
      // editing
      await userServices.updateUser(payload.id, payload)
      toastUtility.showSuccess(`User updated successfully.`)
    } else {
      // adding
      await authenticationService.register(payload)
      toastUtility.showSuccess(`User added successfully.`)
    }

    loadItems({ page: 1, itemsPerPage: itemsPerPage.value })
  } catch (error) {
    toastUtility.showError(error)
  } finally {
    editingUser.value = null
  }
}


async function handleDeleteConfirm() {
  try {
    await userServices.deleteUser(userToDelete.value.id);
    showDeleteDialog.value = false
    toastUtility.showSuccess(`User has been deleted successfully.`);
    userToDelete.value = null
    loadItems({ page: 1, itemsPerPage: itemsPerPage.value })
  } catch (error) {
    toastUtility.showError(error);
  }
}


</script>

<template>
  <v-app>
    <Header @toggle-drawer="drawer = !drawer"></Header>
    <Sidebar :drawer="drawer" @update:drawer="drawer = $event" />

    <v-main>
      <div class="d-flex justify-center user-add-div">
        <div style="width: 75vw;" class="mt-5">
          <v-row>
            <v-col cols="10">
              <v-text-field width="50vw" v-model="searchQuery" variant="outlined" placeholder="Search user ...." />
            </v-col>
            <v-col cols="2" class="mt-3">
              <v-btn color="#3E4E3C" density="comfortable" @click="showInviteDialog = true">
                Add User
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </div>


      <div class="user-table-div d-flex justify-center align-center">
        <v-card width="75vw" elevation="16">
          <v-data-table-server class="user-table" v-model:items-per-page="itemsPerPage" :headers="headers"
            :items="serverItems" :items-length="totalItems" :loading="loading" item-value="name"
            @update:options="loadItems">

            <template #item.actions="{ item }">
              <v-menu offset-y transition="scale-transition">
                <template #activator="{ props }">
                  <v-btn v-bind="props" icon size="x-small" variant="text" class="ma-0 pa-0">
                    <v-icon size="20">mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>

                <v-list density="compact">
                  <v-list-item @click="editUser(item)" class="px-4">
                    <v-list-item-title>Edit</v-list-item-title>
                  </v-list-item>

                  <v-list-item @click="deleteUser(item)" class="px-4">
                    <v-list-item-title class="text-red">Delete</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>



          </v-data-table-server>
        </v-card>
      </div>
      <InviteUserDialog v-model="showInviteDialog" @submit="handleInviteSubmit" />
      <InviteUserDialog v-model="showInviteDialog" :editUser="editingUser" @submit="handleInviteSubmit" />
      <DeleteDialog v-model="showDeleteDialog" @submit="handleDeleteConfirm" />
    </v-main>
  </v-app>
</template>

<style scoped>
.user-table-div {
  background-color: #F5F3EF;
}

.user-add-div {
  background-color: #F5F3EF;
}

:deep(.user-table thead th) {
  background-color: #3E4E3C;
  color: #F5F3EF;
}

:deep(.user-table tbody td) {
  background-color: #F5F3EF;
  color: #3E4E3C;
}
</style>
