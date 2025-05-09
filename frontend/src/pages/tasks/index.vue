<script setup>
import { ref, watch, onMounted } from 'vue'
import { taskServices } from '@/services/tasks'
import { toastUtility } from '@/utilities/toast-utility'
import '@vuepic/vue-datepicker/dist/main.css';
import DateRangePicker from '@/shared/DateRangePicker.vue';
import { taskPriorityChoices, taskLifecycleStatusChoices } from '@/utilities/choice-filter-utility'

const tasks = ref([])
const loading = ref(false)
const totalItems = ref(0)
const currentPage = ref(1)
const itemsPerPage = ref(5)
const searchQuery = ref('')
const filterpriorityQuery = ref([])
const filterStatusQuery = ref([])
const selectedDateRange = ref({
  start_date: null,
  end_date: null,
})

const formatDate = (date) => new Date(date).toLocaleDateString()
const isOverdue = (deadline) => new Date(deadline) < new Date()

const getPriorityColor = (priority) => {
  switch (priority) {
    case 1: return 'green'
    case 2: return 'blue'
    case 3: return 'orange'
    case 4: return 'red'
    default: return 'grey'
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 1: return 'grey'
    case 2: return 'blue'
    case 3: return 'orange'
    case 4: return 'green'
    default: return 'grey'
  }
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await taskServices.getTaskList({
      search: searchQuery.value,
      priority: filterpriorityQuery.value,
      lifecycle_stage: filterStatusQuery.value,
      start_date: selectedDateRange.value.start_date,
      end_date: selectedDateRange.value.end_date,
      page: currentPage.value,
      page_size: itemsPerPage.value,
    })
    tasks.value = response.data.results
    totalItems.value = response.data.count
  } catch (error) {
    toastUtility.showError(error)
  } finally {
    loading.value = false
  }
}

watch([searchQuery, filterpriorityQuery, filterStatusQuery, selectedDateRange, currentPage, itemsPerPage], fetchTasks)
onMounted(fetchTasks)
</script>

<template>
  <v-app class="page-color">
    <v-main>
      <v-container class="mt-3">
        <v-row>
          <v-col cols="4">
            <v-select v-model="filterpriorityQuery" :items="taskPriorityChoices" item-title="value" item-value="key"
              placeholder="Filter by priority" variant="outlined" multiple chips clearable dense />
          </v-col>

          <v-col cols="4">
            <v-select v-model="filterStatusQuery" :items="taskLifecycleStatusChoices" item-title="value"
              item-value="key" placeholder="Filter by task status" variant="outlined" multiple chips clearable dense />
          </v-col>

          <v-col cols="4">
            <DateRangePicker id="task-date" name="task-date" placeholder="Filter by date range" :isRequired="false"
              :modelValue="selectedDateRange" @update:modelValue="val => selectedDateRange = val" />
          </v-col>
        </v-row>

        <v-divider />
        <div class="d-flex justify-space-between mt-5">
          <div style="width: 75vw;">
            <v-row>
              <v-col cols="10">
                <v-text-field v-model="searchQuery" variant="outlined" placeholder="Search user ...." />
              </v-col>
              <v-col cols="2" class="mt-3">
                <v-btn color="#3E4E3C" density="comfortable" @click="showInviteDialog = true">
                  Add User
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </div>

        <v-row justify="center">
          <!-- Task Cards -->
          <v-col cols="12">
            <v-row >
              <v-col cols="12" v-for="(task, index) in tasks" :key="index">
                <v-card :elevation="6" class="pa-4 rounded-xl"
                  style="background-color: #F5F3EF; color: #3E4E3C; border-left: 6px solid #3E4E3C;">

                  <div class="d-flex justify-space-between align-center mb-2">
                    <div>
                      <h4 class="font-weight-bold mb-1">{{ task.title }}</h4>
                      <p class="mb-1">
                        {{ task.description.length > 70 ? task.description.slice(0, 70) + '....' : task.description }}
                      </p>

                    </div>
                    <div>
                      <v-chip size="small" class="text-white mx-3" :color="getPriorityColor(task.priority)"
                        variant="flat">
                        {{
                          taskPriorityChoices.find(p => p.key == task.priority)?.value || 'Unknown'
                        }}
                      </v-chip>
                      <v-chip size="small" class="text-white" :color="getStatusColor(task.lifecycle_stage)"
                        variant="flat">
                        {{
                          taskLifecycleStatusChoices.find(p => p.key == task.lifecycle_stage)?.value || 'Unknown'
                        }}
                      </v-chip>
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
                    </div>
                  </div>

                  <v-divider class="my-2" />

                  <div class="d-flex flex-wrap justify-start text-caption">
                    <v-row>
                      <v-col cols="6">
                        <p><strong>Deadline:</strong> {{ formatDate(task.deadline) }}</p>
                      </v-col>
                      <v-col cols="6" v-if="task.assigned_to">
                        <p>
                          <strong>Assigned:</strong> {{ task.assigned_to.user.username }}
                        </p>
                      </v-col>
                      <v-col cols="6">
                        <p>
                          <strong>Creator:</strong> {{ task.created_by.user.username }} ({{ task.created_by.role }})
                        </p>
                      </v-col>
                      <v-col cols="6" v-if="task.collaborated_with.length">
                        <p>
                          <strong>Collaborators:</strong>
                          {{task.collaborated_with.map(c => c.user.username).join(', ')}}
                        </p>
                      </v-col>
                    </v-row>
                    <div>
                    </div>
                  </div>
                </v-card>
              </v-col>
            </v-row>

            <!-- Pagination -->
            <v-row class="mb-4 d-flex justify-end align-center">
              <v-col cols="auto">
                <span><strong>Items per page:</strong></span>
              </v-col>
              <v-col cols="auto">
                <v-select v-model="itemsPerPage" :items="[5, 10, 20, 50]" dense hide-details variant="outlined"
                  style="max-width: 100px;" />
              </v-col>
              <v-col cols="auto">
                <span>{{ (currentPage - 1) * itemsPerPage + 1 }} -
                  {{ Math.min(currentPage * itemsPerPage, totalItems) }}
                  of {{ totalItems }}
                </span>
              </v-col>
              <v-col cols="auto">
                <v-pagination v-model="currentPage" :length="Math.ceil(totalItems / itemsPerPage)" color="#3E4E3C"
                  density="comfortable" />
              </v-col>
            </v-row>

          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>


<style scoped></style>
