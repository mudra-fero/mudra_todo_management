<script>
import { taskServices } from '@/services/tasks';
import { userServices } from '@/services/users';
import { toastUtility } from '@/utilities/toast-utility';
import { taskPriorityChoices, taskLifecycleStatusChoices } from '@/utilities/choice-filter-utility';
import { userRoleChoices } from '@/utilities/choice-filter-utility';
import DateRangePicker from '@/shared/DateRangePicker.vue';
import AddEditTaskDialog from './components/add-edit-task.vue';
// import DeleteDialog from './components/delete-task.vue';
// import AssignTaskDialog from './components/assign-collab-task.vue';

export default {
    components: {
        DateRangePicker,
        AddEditTaskDialog,
        // DeleteDialog,
        // AssignTaskDialog,
    },
    data() {
        return {
            tasks: [],
            loading: false,
            totalItems: 0,
            currentPage: 1,
            itemsPerPage: 10,
            searchQuery: '',
            filters: {
                priority: [],
                status: [],
                dateRange: {
                    start_date: null,
                    end_date: null,
                },
            },
            showInviteDialog: false,
            editingTask: null,
            showAssignDialog: false,
            selectedTask: null,
            assignOrCollabType: 'assign',
            showDeleteDialog: false,
            taskToDelete: null,
            currentUserRole: '',
            tableHeaders: [
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
        };
    },
    computed: {
        taskPriorityChoices() {
            return taskPriorityChoices;
        },
        taskLifecycleStatusChoices() {
            return taskLifecycleStatusChoices;
        },
    },
    methods: {
        async fetchTasks() {
            this.loading = true;
            try {
                const limit = this.itemsPerPage;
                const offset = (this.currentPage - 1) * limit;

                const response = await taskServices.getTaskList({
                    search: this.searchQuery,
                    priority: this.filters.priority.join(','),
                    lifecycle_stage: this.filters.status.join(','),
                    start_date: this.filters.dateRange.start_date,
                    end_date: this.filters.dateRange.end_date,
                    limit: limit,
                    offset: offset,
                });

                this.tasks = response.data.results;
                this.totalItems = response.data.count;
            } catch (error) {
                toastUtility.showError(error);
            } finally {
                this.loading = false;
            }
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            await this.fetchTasks();
        },
        getPriorityColor(priority) {
            switch (priority) {
                case 1: return 'green';
                case 2: return 'blue';
                case 3: return 'orange';
                case 4: return 'red';
                default: return 'grey';
            }
        },
        getStatusColor(status) {
            switch (status) {
                case 1: return 'grey';
                case 2: return 'blue';
                case 3: return 'orange';
                case 4: return 'green';
                default: return 'grey';
            }
        },
        async onSearchDebounced() {
            this.currentPage = 1
            await this.fetchTasks()
        },
        editTask(task) {
            this.editingTask = { ...task };
            this.showInviteDialog = true;
        },
        openAssignDialog(task, type = 'assign') {
            this.selectedTask = { ...task };
            this.assignOrCollabType = type;
            this.showAssignDialog = true;
        },
        handleDialogClose(val) {
            this.showInviteDialog = val;
        },
        async submitHandler() {
            await this.fetchTasks();
        },
        deleteUser(task) {
            this.taskToDelete = task;
            this.showDeleteDialog = true;
        },
        async handleDeleteConfirm() {
            this.showDeleteDialog = false;
            await this.fetchTasks();
        },
        goToTaskDetails(event, row) {
            const task = row?.item ?? event;
            const taskId = task?.id;
            if (taskId) {
                this.$router.push({ name: 'TaskDetail', params: { id: taskId } });
            } else {
                toastUtility.showError("Unable to extract task ID:", row);
            }
        },
        async handleItemsPerPageChange(newSize) {
            this.currentPage = 1;
            this.itemsPerPage = newSize;
            await this.fetchTasks();
        },
        isAllowed(allowedRoles) {
            return allowedRoles.includes(this.currentUserRole);
        },
    },
    async mounted() {
        await this.fetchTasks();
        const response = await userServices.getCurrentUser();
        this.currentUserRole = userRoleChoices.find(c => c.key === response.data[0].role)?.value;
    },
};
</script>

<template>
    <v-app class="page-color">
        <v-main>
            <v-container class="mt-3">
                <v-row>
                    <v-col cols="4">
                        <v-select v-model="filters.priority"
                            @update:modelValue="() => { currentPage = 1; fetchTasks(); }" density="compact"
                            :items="taskPriorityChoices" item-title="value" item-value="key"
                            placeholder="Filter by priority" label="Filter by priority" variant="outlined" multiple
                            chips clearable dense />
                    </v-col>

                    <v-col cols="4">
                        <v-select v-model="filters.status" @update:modelValue="() => { currentPage = 1; fetchTasks(); }"
                            density="compact" :items="taskLifecycleStatusChoices" item-title="value" item-value="key"
                            placeholder="Filter by task status" label="Filter by task status" variant="outlined"
                            multiple chips clearable dense />
                    </v-col>

                    <v-col cols="4">
                        <DateRangePicker id="task-date" name="task-date" placeholder="Filter by date range"
                            :modelValue="filters.dateRange"
                            @update:modelValue="val => { filters.dateRange = val; currentPage = 1; fetchTasks(); }"
                            label="Filter by date range" :isRequired="false" />
                    </v-col>
                </v-row>

                <v-divider />
                <div class="d-flex justify-space-between mt-5">
                    <div style="width: 75vw;">
                        <v-row>
                            <v-col cols="10">
                                <v-text-field v-model="searchQuery"
                                    v-debounce:input="{ handler: onSearchDebounced, delay: 500 }" variant="outlined"
                                    placeholder="Search task ...." />
                            </v-col>
                            <v-col cols="2" class="mt-3">
                                <v-btn color="#3E4E3C" density="comfortable" v-if="isAllowed(['Admin', 'Manager'])"
                                    @click="showInviteDialog = true">
                                    Add Task
                                </v-btn>
                            </v-col>
                        </v-row>
                    </div>
                </div>

                <!-- Task Table -->
                <v-card elevation="16" class="mb-3">
                    <v-data-table-server @click:row="goToTaskDetails" @update:page="handlePageChange"
                        @update:items-per-page="handleItemsPerPageChange" :headers="tableHeaders" :items="tasks"
                        :loading="loading" class="task-table" :items-length="totalItems">

                        <template #item.sn="{ index }">
                            {{ (currentPage - 1) * itemsPerPage + index + 1 }}
                        </template>

                        <template #item.description="{ item }">
                            {{ item.description?.length > 70 ? item.description.slice(0, 70) + '...' : item.description
                            }}
                        </template>

                        <template #item.priority="{ item }">

                            <v-chip size="small" class="text-white mx-3" :color="getPriorityColor(item.priority)"
                                variant="flat">
                                {{taskPriorityChoices.find(p => String(p.key) === String(item.priority))?.value ||
                                    'Unknown'}}
                            </v-chip>
                        </template>

                        <template #item.lifecycle_stage="{ item }">

                            <v-chip size="small" class="text-white" :color="getStatusColor(item.lifecycle_stage)"
                                variant="flat">
                                {{taskLifecycleStatusChoices.find(s => String(s.key) ===
                                    String(item.lifecycle_stage))?.value ||
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
                                    <v-list-item v-if="isAllowed(['Admin', 'Manager', 'Team Member'])"
                                        @click="editTask(item)" class="px-4">
                                        <v-list-item-title>Edit</v-list-item-title>
                                    </v-list-item>

                                    <v-list-item v-if="isAllowed(['Admin', 'Manager'])"
                                        @click="openAssignDialog(item, 'assign')" class="px-4">
                                        <v-list-item-title>Assign</v-list-item-title>
                                    </v-list-item>

                                    <v-list-item v-if="isAllowed(['Manager'])" @click="openAssignDialog(item, 'collab')"
                                        class="px-4">
                                        <v-list-item-title>Collaborate</v-list-item-title>
                                    </v-list-item>

                                    <v-list-item v-if="isAllowed(['Admin', 'Manager'])" @click="deleteUser(item)"
                                        class="px-4">
                                        <v-list-item-title class="text-red">Delete</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </template>

                    </v-data-table-server>
                </v-card>
            </v-container>

            <!-- Dialog Components -->
            <AddEditTaskDialog v-model="showInviteDialog" :editTask="editingTask" @submit="submitHandler" />


            <!-- <AssignTaskDialog v-if="showAssignDialog" v-model="showAssignDialog" :task="selectedTask" -->
            <!-- :type="assignOrCollabType" @submit="submitHandler" /> -->

            <!-- <DeleteDialog v-if="showDeleteDialog" v-model="showDeleteDialog" :task="taskToDelete" -->
            <!-- @confirm="handleDeleteConfirm" /> -->
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