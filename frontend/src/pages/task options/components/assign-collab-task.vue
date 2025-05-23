<script>
import { userServices } from '@/services/users'
import { taskServices } from '@/services/tasks'
import { toastUtility } from '@/utilities/toast-utility'
import { userRoleChoices } from '@/utilities/choice-filter-utility'

export default {
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    taskObject: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      default: 'assign'
    }
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      isOpen: this.modelValue,
      users: [],
      assignCollabForm: {
        assigned_to: null,
        collaborated_with: []
      },
      search: '',
      currentUserRole: ''
    }
  },
  computed: {
    filteredUsers() {
      if (!this.search) return this.users
      return this.users.filter(user =>
        user.username.toLowerCase().includes(this.search.toLowerCase())
      )
    },
    isAllSelected() {
      if (!this.filteredUsers.length) return false
      return this.filteredUsers.every(user =>
        this.assignCollabForm.collaborated_with.some(selected => selected.id === user.id)
      )
    }
  },
  watch: {
    modelValue(val) {        
      this.isOpen = val
    },
    isOpen(val) {        
      this.$emit('update:modelValue', val)
    },
    taskObject: {
      immediate: true,
      handler(task) {
        if (!task) return
        this.assignCollabForm.assigned_to = this.users.find(
          user => user.id === task?.assigned_to?.user?.id
        ) || null

        this.assignCollabForm.collaborated_with = (task?.collaborated_with || [])
          .map(collab => this.users.find(user => user.id === collab.user.id))
          .filter(Boolean)
      }
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await userServices.getCurrentUser()
        this.currentUserRole = userRoleChoices.find(c => c.key === response.data[0].role)?.value

        if (['Admin', 'Manager'].includes(this.currentUserRole)) {
          const res = await userServices.getAllUserList()
          this.users = res.data
        }
      } catch (e) {
        toastUtility.showError('Failed to load users.')
      }
    },
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.assignCollabForm.collaborated_with = this.assignCollabForm.collaborated_with.filter(
          selected => !this.filteredUsers.some(user => user.id === selected.id)
        )
      } else {
        const newUsers = this.filteredUsers.filter(
          user => !this.assignCollabForm.collaborated_with.some(selected => selected.id === user.id)
        )
        this.assignCollabForm.collaborated_with = [...this.assignCollabForm.collaborated_with, ...newUsers]
      }
    },
    resetForm() {
      this.assignCollabForm.assigned_to = ''
      this.assignCollabForm.collaborated_with = ''
    },
    closeDialog() {
      this.$emit('update:modelValue', false)
    },
    formCancel() {
      this.resetForm()
      this.closeDialog()
      this.$emit('update:modelValue', false)
    },
    async handleSubmit() {
      try {
        if (this.type === 'assign') {
          await taskServices.assignTask(this.taskObject.id, {
            user_id: this.assignCollabForm.assigned_to.id
          })
          toastUtility.showSuccess('Task Assigned successfully.')
        } else if (this.type === 'collab') {
          await taskServices.collaborateTask(this.taskObject.id, {
            user_ids: this.assignCollabForm.collaborated_with.map(user => user.id)
          })
          toastUtility.showSuccess('Task collaborated successfully.')
        }
        this.$emit('submit')
        this.closeDialog()
      } catch (err) {
        toastUtility.showError(err)
      }
    }
  },
  mounted() {
    this.fetchUsers()
  }
}
</script>

<template>
    <v-dialog v-model="isOpen" max-width="550" persistent>
        
        <v-card style="background-color: #F5F3EF">
            <v-card-title class="text-h5 text-center">
                {{ type === 'assign' ? 'Assign Task' : 'Add Collaborators' }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-form @submit.prevent="handleSubmit">
                    <v-select v-if="type === 'assign'" v-model="assignCollabForm.assigned_to"
                        :items="filteredUsers" item-title="username" item-value="id" label="Assign To" return-object
                        variant="outlined" class="mb-4">
                        <template v-slot:prepend-item>
                            <v-text-field v-model="search" placeholder="Search users..." density="compact"
                                variant="plain" class="px-3" />
                            <v-divider class="mt-2"></v-divider>
                        </template>
                    </v-select>
                    <v-select v-if="type === 'collab'" v-model="assignCollabForm.collaborated_with"
                        :items="filteredUsers" item-title="username" item-value="id" label="Collaborators" multiple
                        return-object class="mb-4" variant="outlined">
                        <template v-slot:prepend-item>
                            <v-text-field v-model="search" placeholder="Search..." density="compact" variant="plain"
                                class="px-3" />
                            <v-divider class="mt-2"></v-divider>
                            <v-list-item @click="toggleSelectAll">
                                <v-list-item-title>
                                    {{ isAllSelected ? 'Deselect All' : 'Select All' }}
                                </v-list-item-title>
                            </v-list-item>
                            <v-divider class="mb-2"></v-divider>
                        </template>
                    </v-select>

                    <v-divider class="mt-3"></v-divider>
                    <v-row class="mt-3">
                        <v-col col="auto">
                            <v-btn type="submit" color="#3E4E3C" block>
                                submit
                            </v-btn>
                        </v-col>
                        <v-col col="auto">
                            <v-btn type="button" color="grey" block @click="formCancel()">
                                Cancel
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>