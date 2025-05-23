<script>
import { useVuelidate } from '@vuelidate/core';
import { required, helpers } from '@vuelidate/validators';
import { toastUtility } from '@/utilities/toast-utility';
import { taskLifecycleStatusChoices, taskPriorityChoices } from '@/utilities/choice-filter-utility';
import { taskServices } from '@/services/tasks';

export default {
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
    editTask: {
      type: [Object, null],
      nullable: true,
      default: null,
    },
  },
  emits: ['update:modelValue', 'submit', 'close'],
  data() {
    return {
      isOpen: this.modelValue,
      taskForm: {
        title: '',
        description: '',
        priority: '',
        lifecycle: '',
        deadline: new Date(),
      },
      showError: false,
      taskPriorityChoices,
      taskLifecycleStatusChoices,
      v$: null,
    };
  },
  computed: {
    isEditMode() {
      return !!this.editTask;
    },
  },
  watch: {
    modelValue(val) {
      this.isOpen = val;
    },
    isOpen(val) {
      this.$emit('update:modelValue', val);
    },
    editTask: {
      immediate: true,
      handler(val) {
        if (val) {
          this.taskForm.title = val.title;
          this.taskForm.description = val.description;
          this.taskForm.priority = String(val.priority);
          this.taskForm.lifecycle = String(val.lifecycle_stage);
          this.taskForm.deadline = new Date(val.deadline);
        } else {
          this.resetForm();
        }
      },
    },
  },
  validations() {
    return {
      taskForm: {
        title: { required: helpers.withMessage('Title is required', required) },
        description: { required: helpers.withMessage('Description is required', required) },
        priority: { required: helpers.withMessage('Priority is required', required) },
        deadline: { required: helpers.withMessage('Deadline is required', required) },
        lifecycle: { required: helpers.withMessage('Lifecycle is required', required) },
      },
    };
  },
  methods: {
    resetForm() {
      this.taskForm.title = null;
      this.taskForm.description = null;
      this.taskForm.priority = null;
      this.taskForm.lifecycle = null;
      this.taskForm.deadline = new Date();
      this.showError = false;
      if (this.v$) this.v$.$reset();
    },
    async handleInviteSubmit() {
      const isValid = await this.v$.$validate();
      if (!isValid) {
        this.showError = true;
        return;
      }
      const payload = {
        title: this.taskForm.title,
        description: this.taskForm.description,
        priority: this.taskForm.priority,
        lifecycle_stage: this.taskForm.lifecycle,
        deadline: this.taskForm.deadline?.toISOString().split('T')[0],
      };
      try {
        if (this.isEditMode) {
          await taskServices.updateTask(this.editTask.id, payload);
          toastUtility.showSuccess('Task updated successfully.');
        } else {
          await taskServices.addTask(payload);
          toastUtility.showSuccess('Task added successfully.');
        }

        this.$emit('submit');
        this.$emit('update:modelValue', false);
        this.resetForm();
      } catch (error) {
        toastUtility.showError(error);
      }
    },
    formCancel() {
      this.resetForm();
      this.$emit('update:modelValue', false);
    },
  },
  mounted() {
    this.v$ = useVuelidate(this.$options.validations.call(this), this);
  },
};
</script>

<template>
  <v-dialog v-model="isOpen" persistent max-width="500px">
    <v-card style="background-color: #F5F3EF">
      <v-card-title class="text-h5 d-flex justify-center">Fill task details</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form @submit.prevent="handleInviteSubmit">
          <v-label class="mb-1">Title</v-label>
          <v-text-field v-model="taskForm.title" placeholder="Enter title" :error="v$?.taskForm?.title?.$error"
            :error-messages="v$?.taskForm?.title?.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Description</v-label>
          <v-textarea v-model="taskForm.description" placeholder="Enter description"
            :error="v$?.taskForm?.description?.$error"
            :error-messages="v$?.taskForm?.description?.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Priority</v-label>
          <v-select v-model="taskForm.priority" :items="taskPriorityChoices" item-title="value" item-value="key"
            variant="outlined" :error="v$?.taskForm?.priority?.$error"
            :error-messages="v$?.taskForm?.priority?.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Lifecycle status</v-label>
          <v-select v-model="taskForm.lifecycle" :items="taskLifecycleStatusChoices" item-title="value" item-value="key"
            variant="outlined" :error="v$?.taskForm?.lifecycle?.$error"
            :error-messages="v$?.taskForm?.lifecycle?.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Deadline</v-label>
          <VueDatePicker v-model="taskForm.deadline" variant="outlined" :error="v$?.taskForm?.deadline?.$error"
            :error-messages="v$?.taskForm?.deadline?.$errors.map(e => e.$message)" placeholder="Deadline"
            :enable-time-picker="false" />

          <v-divider class="mt-3"></v-divider>
          <v-row class="mt-3">
            <v-col col="auto">
              <v-btn type="submit" color="#3E4E3C" block>
                {{ isEditMode ? 'Update' : 'Add' }}
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