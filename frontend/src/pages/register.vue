<script setup>
import { reactive, ref } from 'vue'
import useVuelidate from '@vuelidate/core'
import { required, email as emailValidator } from '@vuelidate/validators'
import { authenticationService } from '@/services/authentication'
import { toastUtility } from '@/utilities/toast-utility'
import { useRouter } from 'vue-router';
const router = useRouter();

const registerForm = reactive({
    username: null,
    password: null,
    email: null,
})

const rules = reactive({
    username: { required },
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
        toastUtility.showError("Please correct all the errors to submit the form!");
        return;
    }

    showError.value = false
    loading.value = true

    try {
        let { data } = await authenticationService.register(registerForm);
        router.push({ name: "login" });
    } catch (error) {
        toastUtility.showError(error);
    }
}
</script>

<template>
    <div class="d-flex align-center justify-center card-div">
        <v-card :disabled="loading" :loading="loading" width="30vw" elevation="16" color="#F5F3EF">
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
                    <v-text-field v-model="registerForm.username" placeholder="Enter username"
                        :error="v$.username.$error" :error-messages="v$.username.$errors.map(e => e.$message)" />

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

                    <v-btn type="submit" color="#3E4E3C" block class="mt-4">
                        Register
                    </v-btn>
                </v-form>

                <v-card-text class="mt-4">
                    or if you have registered already then
                </v-card-text>

                <v-btn color="#3E4E3C" block @click="$router.push('/')">
                    Login
                </v-btn>
            </v-card-text>
        </v-card>
    </div>
</template>

<style scoped>
.card-div {
    height: 100vh;
    background-color: #3E4E3C;
}
</style>
