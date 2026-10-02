<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center px-4">
    <div class="w-full max-w-md">

      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white">
          Request Admin Access
        </h1>

        <p class="mt-2 text-slate-400">
          Submit a request to manage Counting Stars.
        </p>
      </div>

      <!-- Card -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <!-- Success -->
        <div
          v-if="success"
          class="rounded-lg border border-green-500/30
                 bg-green-500/10 p-4 text-green-400"
        >
          {{ success }}

          <RouterLink
            to="/admin/login"
            class="mt-4 block font-semibold text-green-300 hover:text-green-200"
          >
            Go to Admin Login →
          </RouterLink>
        </div>

        <!-- Form -->
        <form
          v-else
          @submit.prevent="submitRequest"
          class="space-y-5"
        >

          <!-- Username -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Username
            </label>

            <input
              v-model="form.username"
              type="text"
              required
              minlength="3"
              maxlength="50"
              placeholder="Enter username"
              class="w-full rounded-lg border border-slate-700
                     bg-slate-950 px-4 py-3 text-white
                     outline-none transition
                     focus:border-yellow-400"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Password
            </label>

            <input
              v-model="form.password"
              type="password"
              required
              minlength="8"
              placeholder="Minimum 8 characters"
              class="w-full rounded-lg border border-slate-700
                     bg-slate-950 px-4 py-3 text-white
                     outline-none transition
                     focus:border-yellow-400"
            />
          </div>

          <!-- Reason -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Why do you need admin access?
            </label>

            <textarea
              v-model="form.reason"
              required
              rows="4"
              placeholder="Tell the clan leadership why you need access..."
              class="w-full resize-none rounded-lg border border-slate-700
                     bg-slate-950 px-4 py-3 text-white
                     outline-none transition
                     focus:border-yellow-400"
            ></textarea>
          </div>

          <!-- Error -->
          <div
            v-if="error"
            class="rounded-lg border border-red-500/30
                   bg-red-500/10 p-3 text-sm text-red-400"
          >
            {{ error }}
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full rounded-lg bg-yellow-400
                   px-4 py-3 font-bold text-slate-950
                   transition hover:bg-yellow-300
                   disabled:cursor-not-allowed
                   disabled:opacity-50"
          >
            {{ loading ? 'Submitting...' : 'Request Admin Access' }}
          </button>

        </form>

        <!-- Login -->
        <div
          v-if="!success"
          class="mt-6 text-center text-sm text-slate-500"
        >
          Already have an admin account?

          <RouterLink
            to="/admin/login"
            class="font-semibold text-yellow-400 hover:text-yellow-300"
          >
            Login
          </RouterLink>
        </div>

      </div>

      <!-- Note -->
      <p class="mt-5 text-center text-xs text-slate-600">
        Admin requests are reviewed by Counting Stars leadership.
      </p>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '../../services/api'

const form = reactive({
  username: '',
  password: '',
  reason: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

async function submitRequest() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.post('/auth/register', {
      username: form.username.trim(),
      password: form.password,
      reason: form.reason.trim()
    })

    success.value =
      response.data.message ||
      'Your admin registration request has been submitted.'

    form.username = ''
    form.password = ''
    form.reason = ''

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to submit the request. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>