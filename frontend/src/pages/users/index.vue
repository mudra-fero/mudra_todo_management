<script setup>
import { ref } from 'vue'
import { watch } from 'vue'
import InviteUserDialog from './components/invite-user.vue'
import DeleteDialog from './components/delete-user.vue'
import { userServices } from '@/services/users'
import { toastUtility } from '@/utilities/toast-utility'
import { userRoleChoices } from '@/utilities/choice-filter-utility'

const showInviteDialog = ref(false)
const itemsPerPage = ref(10)
const serverItems = ref([])
const loading = ref(true)
const totalItems = ref(0)
const searchQuery = ref('')
const filterQuery = ref(null)
const showDeleteDialog = ref(false)
const userToDelete = ref(null)
const editingUser = ref(null)
const changePasswordMode = ref(false)

function changeUserPassword(user) {
  editingUser.value = { ...user }
  changePasswordMode.value = true
  showInviteDialog.value = true
}

function editUser(user) {
  editingUser.value = { ...user }
  showInviteDialog.value = true
}

function deleteUser(user) {
  userToDelete.value = user
  showDeleteDialog.value = true
}

function handleDialogClose(val) {
  showInviteDialog.value = val
  if (!val) {
    editingUser.value = null
    changePasswordMode.value = false
  }
}

watch(searchQuery, () => {
  loadItems({ page: 1, itemsPerPage: itemsPerPage.value })
})

watch(filterQuery, () => {
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

function getColor(role) {
  if (role == "TEAM_MEMBER") return 'error'
  else if (role == "MANAGER") return 'warning'
  else return 'success'
}

const fetchUsers = async (params) => {
  params = {
    ...params,
    search: searchQuery.value,
    filter: filterQuery.value,
    page: params.page,
    page_size: itemsPerPage.value,
  }
  try {
    const response = await userServices.getUserList(params);
    return {
      items: response.data.results,
      total: response.data.count,
    }
  } catch (error) {
    toastUtility.showError(error);
  } finally {
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

async function submitHandler() {
  loadItems({ page: 1, itemsPerPage: itemsPerPage.value })
}
</script>

<template>
  <v-app class="page-color">
    <v-main>
      <div class="d-flex justify-center">
        <div style="width: 75vw;" class="mt-5">
          <v-row>
            <v-col cols="5">
              <v-text-field width="30vw" v-model="searchQuery" variant="outlined" placeholder="Search user ...." />
            </v-col>
            <v-col cols="5">
              <v-select clearable chips placeholder="Select Role" v-model="filterQuery" variant="outlined"
                :items="userRoleChoices" item-title="value" item-value="key" multiple></v-select>
            </v-col>
            <v-col cols="2" class="mt-3">
              <v-btn color="#3E4E3C" density="comfortable" @click="showInviteDialog = true">
                Add User
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </div>


      <div class="d-flex justify-center align-center">
        <v-card width="75vw" elevation="16">
          <v-data-table-server height="60vh" class="user-table" v-model:items-per-page="itemsPerPage" :headers="headers"
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

                  <v-list-item @click="changeUserPassword(item)" class="px-4">
                    <v-list-item-title>Change password</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>

            <template #item.role="{ item }">
              <v-chip :border="`${getColor(item.role)} thin opacity-25`" :color="getColor(item.role)" :text="item.role"
                size="x-small"></v-chip>
            </template>


          </v-data-table-server>
        </v-card>
      </div>
      <InviteUserDialog v-model="showInviteDialog" :editUser="editingUser" :changePasswordMode="changePasswordMode"
        @submit="submitHandler()" @update:modelValue="handleDialogClose" />
      <DeleteDialog v-model="showDeleteDialog" @submit="handleDeleteConfirm" />
    </v-main>
  </v-app>
</template>

<style scoped>
:deep(.user-table thead th) {
  background-color: #3E4E3C;
  color: #F5F3EF;
}

:deep(.user-table tbody td) {
  background-color: #F5F3EF;
  color: #3E4E3C;
}
</style>
