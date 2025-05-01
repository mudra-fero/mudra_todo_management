<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Header from '@/layout/Header.vue'
import Sidebar from '@/layout/Sidebar.vue'
import { watch } from 'vue'

const drawer = ref(true)
const itemsPerPage = ref(10)
const serverItems = ref([])
const loading = ref(true)
const totalItems = ref(0)
const searchQuery = ref('')

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

async function fetchCars({ page, itemsPerPage, sortBy }) {
  const token = localStorage.getItem('access_token')
  try {
    const response = await axios.get('http://127.0.0.1:8000/users/', {
      params: {
        page,
        per_page: itemsPerPage,
        search: searchQuery.value
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return {
      items: response.data.results,
      total: response.data.count,
    }

  } catch (error) {
    console.error('Failed to fetch cars:', error)
    return { items: [], total: 0 }
  }
}

function loadItems({ page, itemsPerPage, sortBy }) {
  loading.value = true
  fetchCars({ page, itemsPerPage, sortBy }).then(({ items, total }) => {
    serverItems.value = items.map((item, index) => ({
      ...item,
      sn: (page - 1) * itemsPerPage + index + 1,
    }))
    totalItems.value = total
    loading.value = false
  })
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
              <v-btn color="#3E4E3C" density="comfortable">Invite User</v-btn>
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
              <v-icon icon="mdi-pencil" size="small" color="#3E4E3C" class="me-2" @click="editUser(item)" />
              <v-icon icon="mdi-delete" size="small" color="red" @click="deleteUser(item)" />
            </template>

          </v-data-table-server>
        </v-card>
      </div>
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
