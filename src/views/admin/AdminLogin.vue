<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ShieldCheck, LockKeyhole, User } from 'lucide-vue-next'
import api from '../../services/api'

const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const login = async () => {
  error.value = ''

  if (!username.value || !password.value) {
    error.value = 'Please enter your username and password.'
    return
  }

  loading.value = true

  try {
    const response = await api.post(
      '/auth/login',
      {
        username: username.value,
        password: password.value
      }
    )

    if (response.data.success) {
      localStorage.setItem(
        'admin_token',
        response.data.token
      )

      localStorage.setItem(
        'admin_user',
        JSON.stringify(response.data.user)
      )

      router.push('/admin')
    }
  } catch (err) {
    console.error('Login failed:', err)

    error.value =
      err.response?.data?.error ||
      'Unable to login. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="flex min-h-[calc(100vh-100px)] items-center
           justify-center bg-[#080b12] px-6 py-12"
  >

    <div class="w-full max-w-md">

      <!-- Logo -->
      <div class="mb-8 text-center">

        <div
          class="mx-auto flex h-16 w-16 items-center
                 justify-center rounded-2xl
                 bg-yellow-400 text-3xl
                 shadow-lg shadow-yellow-400/20"
        >
          🛡️
        </div>

        <h1 class="mt-5 text-3xl font-black">
          Admin Login
        </h1>

        <p class="mt-2 text-slate-500">
          Counting Stars Headquarters
        </p>

      </div>

      <!-- Login card -->
      <div
        class="rounded-2xl border border-white/10
               bg-slate-900 p-7 shadow-2xl"
      >

        <form
          @submit.prevent="login"
          class="space-y-6"
        >

          <!-- Username -->
          <div>

            <label
              class="mb-2 block text-sm font-medium"
            >
              Username
            </label>

            <div class="relative">

              <User
                class="absolute left-4 top-1/2
                       h-5 w-5 -translate-y-1/2
                       text-slate-500"
              />

              <input
                v-model="username"
                type="text"
                autocomplete="username"
                placeholder="Enter username"
                class="w-full rounded-xl border
                       border-slate-700 bg-slate-950
                       py-3 pl-12 pr-4 text-white
                       outline-none transition
                       placeholder:text-slate-600
                       focus:border-yellow-400"
              />

            </div>

          </div>

          <!-- Password -->
          <div>

            <label
              class="mb-2 block text-sm font-medium"
            >
              Password
            </label>

            <div class="relative">

              <LockKeyhole
                class="absolute left-4 top-1/2
                       h-5 w-5 -translate-y-1/2
                       text-slate-500"
              />

              <input
                v-model="password"
                type="password"
                autocomplete="current-password"
                placeholder="Enter password"
                class="w-full rounded-xl border
                       border-slate-700 bg-slate-950
                       py-3 pl-12 pr-4 text-white
                       outline-none transition
                       placeholder:text-slate-600
                       focus:border-yellow-400"
              />

            </div>

          </div>

          <!-- Error -->
          <div
            v-if="error"
            class="rounded-xl border
                   border-red-900 bg-red-950/40
                   px-4 py-3 text-sm text-red-300"
          >
            {{ error }}
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="flex w-full items-center
                   justify-center gap-2 rounded-xl
                   bg-yellow-400 px-6 py-3.5
                   font-bold text-black transition
                   hover:bg-yellow-300
                   disabled:cursor-not-allowed
                   disabled:opacity-60"
          >

            <ShieldCheck class="h-5 w-5" />

            {{
              loading
                ? 'Signing in...'
                : 'Sign In'
            }}

          </button>

        </form>

      </div>

      <!-- Back -->
      <div class="mt-6 text-center">

        <RouterLink
          to="/"
          class="text-sm text-slate-500
                 transition hover:text-white"
        >
          ← Back to Counting Stars
        </RouterLink>

      </div>

    </div>

  </div>
</template>