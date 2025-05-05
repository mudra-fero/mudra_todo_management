<script setup>
import { ref, reactive, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email as emailValidator } from '@vuelidate/validators'
import { toastUtility } from '@/utilities/toast-utility'
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  editUser: Object
})

const emit = defineEmits(['update:modelValue', 'submit', 'close'])
const isEditMode = computed(() => !!props.editUser)
const isOpen = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  isOpen.value = val
})

watch(isOpen, (val) => {
  emit('update:modelValue', val)
})

watch(() => props.editUser, (val) => {
  if (val) {
    registerForm.email = val.email || ''
    registerForm.username = val.username || ''
    registerForm.role = val.role || ''
  }
})

const isPasswordVisible = ref(false)

const registerForm = reactive({
  username: '',
  password: '',
  email: '',
  role: ''
})

const showError = ref(false)

const rules = computed(() => ({
  username: { required },
  password: isEditMode.value ? {} : { required },
  email: { required, email: emailValidator },
  role: { required }
}))


function resetForm() {
  registerForm.username = ''
  registerForm.password = ''
  registerForm.email = ''
  registerForm.role = ''
  showError.value = false
  v$.value.$reset()
}

const v$ = useVuelidate(rules, registerForm)

async function sendInvite() {
  v$.value.$touch()
  if (!v$.value.$invalid) {
    showError.value = false

    const payload = {
      ...registerForm,
    }

    if (props.editUser && props.editUser.id) {
      payload.id = props.editUser.id
    }

    emit('submit', payload)
    resetForm()
    emit('update:modelValue', false)
  } else {
    toastUtility.showError("Please correct all the errors to submit the form!");
  }
}

function formCancel() {
  resetForm()
  emit('update:modelValue', false)
}
</script>

<template>
  <v-dialog v-model="isOpen" persistent max-width="500px">
    <v-card style="background-color: #F5F3EF">
      <v-card-title class="text-h5 d-flex justify-center">Fill user details</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form @submit.prevent="sendInvite">
          <v-alert v-if="showError" type="error" icon="$error" class="mb-4">
            Please fill all fields correctly.
          </v-alert>

          <v-label class="mb-1">Email</v-label>
          <v-text-field v-model="registerForm.email" placeholder="Enter email" :error="v$.email.$error"
            :error-messages="v$.email.$errors.map(e => e.$message)" />

          <v-label class="mb-1">Username</v-label>
          <v-text-field v-model="registerForm.username" placeholder="Enter username" :error="v$.username.$error"
            :error-messages="v$.username.$errors.map(e => e.$message)" />

          <v-label v-if="!isEditMode" class="mb-1">Password</v-label>
          <v-text-field v-if="!isEditMode" v-model="registerForm.password"
            :type="isPasswordVisible ? 'text' : 'password'" placeholder="Enter password" :error="v$.password.$error"
            :error-messages="v$.password.$errors.map(e => e.$message)">
            <template #append-inner>
              <v-icon @click="isPasswordVisible = !isPasswordVisible" style="cursor: pointer">
                {{ isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye' }}
              </v-icon>
            </template>
          </v-text-field>


          <v-label class="mb-1">Role</v-label>
          <v-select v-model="registerForm.role" :items="['ADMIN', 'MANAGER', 'TEAM_MEMBER']" label="Select Role"
            variant="outlined" :error="v$.role.$error" :error-messages="v$.role.$errors.map(e => e.$message)" />
          <v-divider></v-divider>
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
