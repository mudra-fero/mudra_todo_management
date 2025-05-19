<script setup>
import { taskPriorityChoices, taskLifecycleStatusChoices } from '@/utilities/choice-filter-utility'
import AddEditTaskDialog from './components/add-edit-task.vue'
import DeleteDialog from './components/delete-task.vue';
import AssignTaskDialog from './components/assign-collab-task.vue';
import { useRoute, useRouter } from 'vue-router';
import { taskServices } from '@/services/tasks'
import { ref, watch, nextTick, onMounted } from 'vue';
import { userServices } from '@/services/users'
import { toastUtility } from '@/utilities/toast-utility'
import { userRoleChoices } from '@/utilities/choice-filter-utility'

const route = useRoute();
const taskId = route.params.id;
const task = ref(null);
const comments = ref([]);
const logs = ref([]);
const tab = ref('comments');
const showInviteDialog = ref(false)
const assignOrCollabType = ref('assign')
const editingTask = ref(null)
const newComment = ref('')
const commentsContainer = ref(null)
const showAssignDialog = ref(false)
const selectedTask = ref(null)
const currentUserRole = ref('')
const mentionQuery = ref('');
const showMentionList = ref(false);
const mentionIndex = ref(-1);
const usersList = ref([]);
const filteredUsers = ref([]);
const mentionedUsers = ref([]);

watch(comments, async () => {
  await nextTick()
  const el = commentsContainer.value
  if (el) {
    el.scrollTop = el.scrollHeight
  }
})

const fetchTasks = async () => {
  const taskData = await taskServices.getTask(taskId)
  const commentsData = await taskServices.getCommentsList(taskId)
  const historyData = await taskServices.getHistoryList(taskId)

  task.value = taskData.data
  comments.value = commentsData.data
  logs.value = historyData.data
}

function openAssignDialog(task, type = 'assign') {
  selectedTask.value = { ...task }
  assignOrCollabType.value = type
  showAssignDialog.value = true
}

function editTask(task) {
  editingTask.value = { ...task }
  showInviteDialog.value = true
}
const submitHandler = async () => {
  fetchTasks()
}
function handleDialogClose(val) {
  showInviteDialog.value = val
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
const addComment = async () => {
  if (!newComment.value.trim()) return

  try {
    await taskServices.addComments(taskId, { content: newComment.value, user_ids: mentionedUsers.value })
    newComment.value = ''
    await fetchTasks()
  } catch (error) {
    toastUtility.showError(error)
  }
}

const deleteComment = async (commentId) => {
  try {
    await taskServices.deleteComment(taskId, commentId);
    await fetchTasks()
  } catch (error) {
    toastUtility.showError(error)
  }
};

watch(newComment, (val) => {
  const newVal = val.trim();
  const mentionMatch = newVal.match(/@([\w\d_-]*)$/);
  if (mentionMatch) {
    const query = mentionMatch[1];
    mentionQuery.value = query;
    filteredUsers.value = usersList.value.filter(u =>
      u.username.toLowerCase().startsWith(query.toLowerCase())
    );
    showMentionList.value = filteredUsers.value.length > 0;
  } else {
    showMentionList.value = false;
  }
});

function selectMention(username) {
  const atIndex = newComment.value.lastIndexOf('@');
  newComment.value =
    newComment.value.substring(0, atIndex) + username + ' ';

  showMentionList.value = false;
  mentionQuery.value = '';

  const matchedUser = usersList.value.find(u => u.username === username);
  if (matchedUser && !mentionedUsers.value.some(u => u.id === matchedUser.id)) {
    mentionedUsers.value.push(matchedUser.id);
  }
}

onMounted(async () => {
  fetchTasks()
  const response = await userServices.getCurrentUser()
  currentUserRole.value = userRoleChoices.find(c => c.key === response.data[0].role)?.value

  const userRes = await userServices.getUserList();
  usersList.value = userRes.data.results.map(user => ({
    id: user.id,
    username: user.username
  }));
})

const isAllowed = (allowedRoles) => {
  return allowedRoles.includes(currentUserRole.value)
}
</script>

<template>
  <v-app class="page-color">
    <v-main v-if="task">
      <v-container class="py-4 text-forest" style="max-width: 1100px;">
        <div class="mt-3 d-flex justify-space-between">
          <h1 class="title">{{ task.title }}</h1>
          <div class="mt-3">
            <v-menu offset-y transition="scale-transition">
              <template #activator="{ props }">
                <v-btn v-bind="props" icon size="x-small" variant="text" class="ma-0 pa-0">
                  <v-icon size="20">mdi-dots-vertical</v-icon>
                </v-btn>
              </template>

              <v-list density="compact">
                <v-list-item v-if="isAllowed(['Admin', 'Manager', 'Team Member'])" @click="editTask(item)" class="px-4">
                  <v-list-item-title>Edit</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="isAllowed(['Admin', 'Manager'])" @click="openAssignDialog(item, 'assign')"
                  class="px-4">
                  <v-list-item-title>Assign</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="isAllowed(['Manager'])" @click="openAssignDialog(item, 'collab')" class="px-4">
                  <v-list-item-title>Collaborate</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="isAllowed(['Admin', 'Manager'])" @click="deleteUser(item)" class="px-4">
                  <v-list-item-title class="text-red">Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </div>

        <div class="d-flex justify-start mt-2">
          <v-chip class="mr-2">
            {{
              taskPriorityChoices.find(p => String(p.key) === String(task.priority))?.value || 'Unknown'
            }}
          </v-chip>

          <v-chip class="mr-2">
            {{
              taskLifecycleStatusChoices.find(p => String(p.key) === String(task.lifecycle_stage))?.value || 'Unknown'
            }}
          </v-chip>

          <v-chip class="mr-2">
            deadline: {{ task.deadline_humanized }}
          </v-chip>

          <v-chip>
            created: {{ task.created_humanized }}
          </v-chip>
        </div>

        <div class="mt-4 mb-2">
          <p class="mb-0">{{ task.description }}</p>
        </div>

        <p>
          <strong>Assigned:</strong> {{ task.assigned_to?.user?.username || "--" }}
        </p>
        <p>
          <strong>Creator:</strong> {{ task.created_by.user.username }} ({{ task.created_by.role }})
        </p>
        <p>
          <strong>Collaborators:</strong>
          {{task.collaborated_with.map(c => c.user.username).join(', ') || "--"}}
        </p>

        <v-tabs v-model="tab" class="mt-4">
          <v-tab value="comments">comments</v-tab>
          <v-tab v-if="isAllowed(['Admin', 'Manager'])" value="history">history</v-tab>
        </v-tabs>

        <v-card-text>
          <v-tabs-window v-model="tab">
            <v-tabs-window-item value="comments">
              <div ref="commentsContainer" style="max-height: 40vh; overflow-y: auto;" class="border mt-3">
                <v-row v-if="comments.length" class="mt-4 mb-1 mx-2">
                  <v-col cols="12" v-for="(comment, index) in comments" :key="index" :class="[
                    'd-flex',
                    'justify-start'
                  ]">
                    <div class="d-flex align-center justify-start">
                      <v-icon class="mr-3" size="36">mdi-account-circle</v-icon>
                      <v-card-text class="pa-2">
                        <div class="d-flex justify-start align-center">
                          <span class="text-primary font-weight-medium mr-2">
                            {{ comment.author.user.username }}
                          </span>
                          <span class="text-caption text-grey-darken-1">{{ comment.created_humanized }}</span>
                        </div>
                        <div>{{ comment.content }}</div>
                        <span class="ml-auto text-red d-flex justify-end" @click="deleteComment(comment.id)">
                          Delete
                        </span>
                      </v-card-text>
                    </div>
                  </v-col>
                </v-row>
                <v-col cols="12" v-else class="text-center mt-5 mb-5">
                  <v-icon aria-hidden="false">
                    mdi-message-text
                  </v-icon>
                  No comments found.
                </v-col>
              </div>
              <v-row class="mt-2">
                <v-col cols="11">
                  <div style="position: relative;">
                    <v-text-field density="compact" v-model="newComment" variant="outlined" label="Add a comment"
                      placeholder="Write your comment here..." rows="3" auto-grow />
                    <v-list class="listStyle" v-if="showMentionList">
                      <v-list-item v-for="(user, index) in filteredUsers" :key="user.id"
                        @click="selectMention(user.username)" :class="{ 'bg-grey-lighten-3': index === mentionIndex }">
                        <v-list-item-subtitle>@{{ user.username }}</v-list-item-subtitle>
                      </v-list-item>

                    </v-list>
                  </div>
                </v-col>
                <v-col>
                  <v-icon aria-hidden="false" size="40" @click="addComment">
                    mdi-send-circle
                  </v-icon>
                </v-col>
              </v-row>

            </v-tabs-window-item>

            <v-tabs-window-item v-if="isAllowed(['Admin', 'Manager'])" value="history">
              <div style="max-height: 50vh; overflow-y: auto;">
                <v-timeline side="end" class="border">
                  <v-timeline-item v-for="(log, index) in logs" :key="index" :dot-color="'#3E4E3C'" size="small">
                    <v-card color="#F5F3EF" flat>
                      <v-card-text class="border">
                        <v-row>
                          <v-col cols="12">
                            <span class="text-caption text-grey-darken-1">
                              {{ log.created_humanized }}
                            </span>
                            <div>
                              <strong class="text-primary">
                                {{ log.user.user.username }} ({{ log.user.role }})
                              </strong>
                              <div>{{ log.action }}</div>
                            </div>
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </v-timeline-item>
                </v-timeline>
              </div>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card-text>
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
.text-forest {
  color: #3E4E3C !important;
}

.listStyle {
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  z-index: 2000;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>
