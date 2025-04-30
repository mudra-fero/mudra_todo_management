<script setup>
import { reactive, ref } from 'vue'
import useVuelidate from '@vuelidate/core'
import { required, email as emailValidator } from '@vuelidate/validators'
import { authenticationservice } from '@/services/authentication'

const registerForm = reactive({
    userName: null,
    password: null,
    email: null,
})

const rules = reactive({
    userName: { required },
    password: { required },
    email: { required, email: emailValidator },
})
const loading = ref(false)
const isPasswordVisible = ref(false)
const v$ = useVuelidate(rules, registerForm)
const showError = ref(false)

const submit = async () => {
    const isValid = await v$.value.$validate()
    if (!isValid) {
        showError.value = true
        return
    }

    showError.value = false
    loading.value = true
    try {
        const { response } = await authenticationservice.register(registerForm)
        console.log(response);
        
        setTimeout(() => (loading.value = false), 2000)
    } catch {
        alert('error')
    }

    console.log('Form Submitted:', registerForm)
}
</script>

<template>
    <div class="d-flex align-center justify-center card-div">
        <v-card :disabled="loading" :loading="loading" width="30vw">
            <template v-slot:loader="{ isActive }">
                <v-progress-linear :active="isActive" color="deep-purple" height="4" indeterminate></v-progress-linear>
            </template>
            <v-card-item class="d-flex justify-center">
                <v-card-title>Welcome!</v-card-title>
                <v-card-subtitle>Please Register</v-card-subtitle>
            </v-card-item>

            <v-card-text>
                <v-form @submit.prevent="submit">
                    <v-alert v-if="showError" type="error" icon="$error" class="mb-4">
                        Please fill all fields correctly.
                    </v-alert>

                    <v-label class="mb-3 mx-1">Email</v-label>
                    <v-text-field v-model="registerForm.email" placeholder="Enter email" :error="v$.email.$error"
                        :error-messages="v$.email.$errors.map(e => e.$message)" />

                    <v-label class="mb-3 mx-1">Username</v-label>
                    <v-text-field v-model="registerForm.userName" placeholder="Enter username"
                        :error="v$.userName.$error" :error-messages="v$.userName.$errors.map(e => e.$message)" />

                    <v-label class="mb-3 mx-1">Password</v-label>
                    <v-text-field v-model="registerForm.password" :type="isPasswordVisible ? 'text' : 'password'"
                        placeholder="Enter password" :error="v$.password.$error"
                        :error-messages="v$.password.$errors.map(e => e.$message)">
                        <template #append-inner>
                            <v-icon @click="isPasswordVisible = !isPasswordVisible" style="cursor: pointer">
                                {{ isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye' }}
                            </v-icon>
                        </template>
                    </v-text-field>

                    <v-btn type="submit" color="info" block class="mt-4">
                        Register
                    </v-btn>
                </v-form>

                <v-card-text class="mt-4">
                    or if you have registered already then
                </v-card-text>

                <v-btn color="info" block @click="$router.push('/login')">
                    Login
                </v-btn>
            </v-card-text>
        </v-card>
    </div>
</template>

<style scoped>
.card-div {
    height: 100vh;
    background-color: #bbe1ec;
}
</style>
