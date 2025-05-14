<script setup>
import { ref, watch, onMounted } from 'vue'
import { taskServices } from '@/services/tasks'
import { toastUtility } from '@/utilities/toast-utility'
import '@vuepic/vue-datepicker/dist/main.css';
import DateRangePicker from '@/shared/DateRangePicker.vue';
import AddEditTaskDialog from './components/add-edit-task.vue'
import DeleteDialog from './components/delete-task.vue';
import AssignTaskDialog from './components/assign-collab-task.vue';
import { taskPriorityChoices, taskLifecycleStatusChoices } from '@/utilities/choice-filter-utility'
import { useRouter } from 'vue-router';

const router = useRouter();
const tasks = ref([])
const loading = ref(false)
const totalItems = ref(0)
const currentPage = ref(1)
const itemsPerPage = ref(5)
const searchQuery = ref('')
const filterpriorityQuery = ref([])
const filterStatusQuery = ref([])
const showInviteDialog = ref(false)
const editingTask = ref(null)
const isCardView = ref(false)
const assignOrCollabType = ref('assign')
const selectedDateRange = ref({
  start_date: null,
  end_date: null,
})
const formatDate = (date) => new Date(date).toLocaleDateString()

function editTask(task) {
  editingTask.value = { ...task }
  showInviteDialog.value = true
}

const showAssignDialog = ref(false)
const selectedTask = ref(null)

function openAssignDialog(task, type = 'assign') {
  console.log(task);
  
  selectedTask.value = { ...task }
  assignOrCollabType.value = type
  showAssignDialog.value = true
}

function handleDialogClose(val) {
  showInviteDialog.value = val
}

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

const tableHeaders = [
  { title: 'S.No', key: 'sn', align: 'center', sortable: false },
  { title: 'Title', key: 'title', align: 'center', sortable: false },
  { title: 'Description', key: 'description', align: 'center', sortable: false },
  { title: 'Deadline', key: 'deadline', align: 'center', sortable: false },
  { title: 'Assigned To', key: 'assigned_to', align: 'center', sortable: false },
  { title: 'Created By', key: 'created_by', align: 'center', sortable: false },
  { title: 'Collaborators', key: 'collaborated_with', align: 'center', sortable: false },
  { title: 'Priority', key: 'priority', align: 'center', sortable: false },
  { title: 'Status', key: 'lifecycle_stage', align: 'center', sortable: false },
  { title: 'Actions', key: 'actions', align: 'center', sortable: false },
]

const fetchTasks = async () => {
  loading.value = true;
  try {
    const limit = itemsPerPage.value;
    const offset = (currentPage.value - 1) * limit;

    const response = await taskServices.getTaskList({
      search: searchQuery.value,
      priority: filterpriorityQuery.value,
      lifecycle_stage: filterStatusQuery.value,
      start_date: selectedDateRange.value.start_date,
      end_date: selectedDateRange.value.end_date,
      limit: limit,
      offset: offset,
    });

    tasks.value = response.data.results;
    totalItems.value = response.data.count;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loading.value = false;
  }
};

const submitHandler = async () => {
  fetchTasks()
}

const showDeleteDialog = ref(false)
const taskToDelete = ref(null)

function deleteUser(task) {
  taskToDelete.value = task
  showDeleteDialog.value = true
}

function handleDeleteConfirm() {
  showDeleteDialog.value = false
  fetchTasks()
}

function goToTaskDetails(event, row) {
  const task = row?.item ?? event;
  const taskId = task?.id;
  if (taskId) {
    router.push({ name: 'TaskDetail', params: { id: taskId } });
  } else {
    toastUtility.showError("Unable to extract task ID:", row);
  }
}

function handleItemsPerPageChange(newSize) {
  currentPage.value = 1;
  itemsPerPage.value = newSize;
  fetchTasks();
}
onMounted(fetchTasks)
</script>

<template>
  <v-app class="page-color">
    <v-main>
      <v-container class="mt-3">
        <v-row>
          <v-col cols="4">
            <v-select v-model="filterpriorityQuery" @update:modelValue="() => { currentPage = 1; fetchTasks(); }"
              density="compact" :items="taskPriorityChoices" item-title="value" item-value="key"
              placeholder="Filter by priority" label="Filter by priority" variant="outlined" multiple chips clearable
              dense />
          </v-col>

          <v-col cols="4">
            <v-select v-model="filterStatusQuery" @update:modelValue="() => { currentPage = 1; fetchTasks(); }"
              density="compact" :items="taskLifecycleStatusChoices" item-title="value" item-value="key"
              placeholder="Filter by task status" label="Filter by task status" variant="outlined" multiple chips
              clearable dense />
          </v-col>

          <v-col cols="4">
            <DateRangePicker id="task-date" name="task-date" placeholder="Filter by date range"
              @update:modelValue="val => { selectedDateRange = val; currentPage = 1; fetchTasks(); }"
              label="Filter by date range" :isRequired="false" :modelValue="selectedDateRange" />
          </v-col>
        </v-row>

        <v-divider />
        <div class="d-flex justify-space-between mt-5">
          <div style="width: 75vw;">
            <v-row>
              <v-col cols="2">
                <v-btn-toggle v-model="isCardView" @update:modelValue="() => { currentPage = 1; fetchTasks(); }"
                  mandatory class="mb-4" color="#3E4E3C">
                  <v-btn :value="true">
                    <v-icon>mdi-view-grid</v-icon>
                  </v-btn>
                  <v-btn :value="false">
                    <v-icon>mdi-table</v-icon>
                  </v-btn>
                </v-btn-toggle>

              </v-col>
              <v-col cols="8">
                <v-text-field v-model="searchQuery" @update:modelValue="() => { currentPage = 1; fetchTasks(); }"
                  variant="outlined" placeholder="Search user ...." />
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
            <div v-if="isCardView">
              <v-row>
                <v-col cols="12" v-for="(task, index) in tasks" :key="index">
                  <v-card :elevation="6" class="pa-4 rounded-xl" @click="goToTaskDetails(task)"
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
                            <v-list-item @click="editTask(task)" class="px-4">
                              <v-list-item-title>Edit</v-list-item-title>
                            </v-list-item>

                            <v-list-item @click="openAssignDialog(task, 'assign')" class="px-4">
                              <v-list-item-title>Assign</v-list-item-title>
                            </v-list-item>

                            <v-list-item @click="openAssignDialog(task, 'collab')" class="px-4">
                              <v-list-item-title>Collaborate</v-list-item-title>
                            </v-list-item>

                            <v-list-item @click="deleteUser(task)" class="px-4">
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
                          <p><strong>Deadline:</strong> {{ task.deadline_humanized }}</p>
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
            </div>

            <div v-else>
              <!-- Table View -->
              <v-card class="mb-3">
                <v-data-table @click:row="goToTaskDetails" :page="currentPage" :items-per-page="itemsPerPage"
                  :headers="tableHeaders" :items="tasks" :loading="loading" class="task-table"
                  @update:modelValue=fetchTasks @update:items-per-page="handleItemsPerPageChange" hide-default-footer>

                  <template #item.sn="{ index }">
                    {{ (currentPage - 1) * itemsPerPage + index + 1 }}
                  </template>

                  <template #item.description="{ item }">
                    {{ item.description?.length > 70 ? item.description.slice(0, 70) + '...' : item.description }}
                  </template>

                  <template #item.priority="{ item }">

                    <v-chip size="small" class="text-white mx-3" :color="getPriorityColor(item.priority)"
                      variant="flat">
                      {{taskPriorityChoices.find(p => String(p.key) === String(item.priority))?.value || 'Unknown'}}
                    </v-chip>
                  </template>

                  <template #item.lifecycle_stage="{ item }">

                    <v-chip size="small" class="text-white" :color="getStatusColor(item.lifecycle_stage)"
                      variant="flat">
                      {{taskLifecycleStatusChoices.find(s => String(s.key) === String(item.lifecycle_stage))?.value ||
                        'Unknown'}}
                    </v-chip>
                  </template>

                  <template #item.deadline="{ item }">
                    {{ item.deadline_humanized }}
                  </template>

                  <template #item.assigned_to="{ item }">
                    {{ item.assigned_to?.user?.username || '-' }}
                  </template>

                  <template #item.created_by="{ item }">
                    {{ item.created_by?.user?.username || '-' }} ({{ item.created_by?.role || '' }})
                  </template>

                  <template #item.collaborated_with="{ item }">
                    <span v-if="item.collaborated_with.length">
                      {{item.collaborated_with.map(c => c.user.username).join(', ')}}
                    </span>
                  </template>

                  <template #item.actions="{ item }">
                    <v-menu offset-y transition="scale-transition">
                      <template #activator="{ props }">
                        <v-btn v-bind="props" icon size="x-small" variant="text" class="ma-0 pa-0">
                          <v-icon size="20">mdi-dots-vertical</v-icon>
                        </v-btn>
                      </template>

                      <v-list density="compact">
                        <v-list-item @click="editTask(item)" class="px-4">
                          <v-list-item-title>Edit</v-list-item-title>
                        </v-list-item>

                        <v-list-item @click="openAssignDialog(item, 'assign')" class="px-4">
                          <v-list-item-title>Assign</v-list-item-title>
                        </v-list-item>

                        <v-list-item @click="openAssignDialog(item, 'collab')" class="px-4">
                          <v-list-item-title>Collaborate</v-list-item-title>
                        </v-list-item>

                        <v-list-item @click="deleteUser(item)" class="px-4">
                          <v-list-item-title class="text-red">Delete</v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </template>

                </v-data-table>
              </v-card>
            </div>

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
              <v-col cols="4">
                <v-pagination v-model="currentPage" :length="Math.ceil(totalItems / itemsPerPage)"
                  @update:modelValue=fetchTasks color="#3E4E3C" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
      <AddEditTaskDialog v-model="showInviteDialog" :editTask="editingTask" @submit="submitHandler"
        @update:modelValue="handleDialogClose" />
      <DeleteDialog v-model="showDeleteDialog" :taskId="taskToDelete?.id" @submit="handleDeleteConfirm" />
      <AssignTaskDialog v-model="showAssignDialog" :taskObject="selectedTask" :mode="assignOrCollabType"
        @submit="fetchTasks" />
    </v-main>
  </v-app>
</template>


<style scoped>
:deep(.task-table thead th) {
  background-color: #3E4E3C;
  color: #F5F3EF;
}

:deep(.task-table tbody td) {
  background-color: #F5F3EF;
  color: #3E4E3C;
}
</style>
