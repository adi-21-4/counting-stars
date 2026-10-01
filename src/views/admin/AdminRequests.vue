<template>
  <div class="min-h-screen bg-slate-950 px-6 py-10">
    <div class="mx-auto max-w-6xl">

      <!-- Header -->
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-3xl font-bold text-white">
            Admin Requests
          </h1>

          <p class="mt-2 text-slate-400">
            Review requests for Counting Stars admin access.
          </p>
        </div>

        <RouterLink
          to="/admin"
          class="rounded-lg border border-slate-700
                 bg-slate-900 px-4 py-2
                 font-semibold text-slate-300
                 transition hover:border-yellow-400
                 hover:text-yellow-400"
        >
          ← Dashboard
        </RouterLink>
      </div>

      <!-- Error -->
      <div
        v-if="error"
        class="mb-6 rounded-lg border border-red-500/30
               bg-red-500/10 p-4 text-red-400"
      >
        {{ error }}
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="rounded-2xl border border-slate-800
               bg-slate-900 p-10 text-center"
      >
        <p class="text-slate-400">
          Loading admin requests...
        </p>
      </div>

      <!-- Empty -->
      <div
        v-else-if="requests.length === 0"
        class="rounded-2xl border border-slate-800
               bg-slate-900 p-10 text-center"
      >
        <h2 class="text-xl font-bold text-white">
          No Admin Requests
        </h2>

        <p class="mt-2 text-slate-500">
          There are currently no registration requests.
        </p>
      </div>

      <!-- Requests -->
      <div v-else class="space-y-5">

        <div
          v-for="request in requests"
          :key="request.id"
          class="rounded-2xl border border-slate-800
                 bg-slate-900 p-6"
        >

          <!-- Top -->
          <div
            class="flex flex-col gap-4
                   md:flex-row md:items-start
                   md:justify-between"
          >

            <div>
              <div class="flex flex-wrap items-center gap-3">

                <h2 class="text-xl font-bold text-white">
                  {{ request.username }}
                </h2>

                <span
                  class="rounded-full border border-yellow-400/30
                         bg-yellow-400/10 px-3 py-1
                         text-xs font-semibold text-yellow-400"
                >
                  {{ request.requestedRole }}
                </span>

                <span
                  class="rounded-full border border-orange-400/30
                         bg-orange-400/10 px-3 py-1
                         text-xs font-semibold text-orange-400"
                >
                  {{ request.status }}
                </span>

              </div>

              <p class="mt-2 text-sm text-slate-500">
                Requested {{ formatDate(request.createdAt) }}
              </p>
            </div>

          </div>

          <!-- Reason -->
          <div class="mt-5 rounded-xl bg-slate-950 p-4">
            <p class="mb-2 text-sm font-semibold text-slate-400">
              Reason for requesting access
            </p>

            <p class="whitespace-pre-wrap text-slate-300">
              {{ request.reason }}
            </p>
          </div>

          <!-- Actions -->
          <div
            v-if="request.status === 'pending'"
            class="mt-5 flex flex-col gap-3 sm:flex-row"
          >

            <button
              @click="reviewRequest(request.id, 'approved')"
              :disabled="processingId === request.id"
              class="rounded-lg bg-green-500 px-5 py-2.5
                     font-bold text-slate-950
                     transition hover:bg-green-400
                     disabled:cursor-not-allowed
                     disabled:opacity-50"
            >
              {{
                processingId === request.id
                  ? 'Processing...'
                  : 'Approve'
              }}
            </button>

            <button
              @click="reviewRequest(request.id, 'rejected')"
              :disabled="processingId === request.id"
              class="rounded-lg border border-red-500/40
                     bg-red-500/10 px-5 py-2.5
                     font-bold text-red-400
                     transition hover:bg-red-500/20
                     disabled:cursor-not-allowed
                     disabled:opacity-50"
            >
              Reject
            </button>

          </div>

          <!-- Reviewed info -->
          <div
            v-if="request.status !== 'pending'"
            class="mt-5 border-t border-slate-800 pt-4"
          >
            <p class="text-sm text-slate-500">
              Reviewed
              <span v-if="request.reviewedBy">
                by {{ request.reviewedBy }}
              </span>

              <span v-if="request.reviewedAt">
                on {{ formatDate(request.reviewedAt) }}
              </span>
            </p>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const requests = ref([])
const loading = ref(true)
const error = ref('')
const processingId = ref(null)

async function loadRequests() {
  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('admin_token')

    const response = await axios.get('/api/admin/requests', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    requests.value = response.data.requests || []

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load admin requests.'
  } finally {
    loading.value = false
  }
}

async function reviewRequest(id, status) {
  const action =
    status === 'approved'
      ? 'approve this admin request'
      : 'reject this admin request'

  if (!window.confirm(`Are you sure you want to ${action}?`)) {
    return
  }

  processingId.value = id
  error.value = ''

  try {
    const token = localStorage.getItem('admin_token')

    await axios.patch(
      `/api/admin/requests/${id}`,
      { status },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    await loadRequests()

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to process the admin request.'
  } finally {
    processingId.value = null
  }
}

function formatDate(date) {
  if (!date) return 'Unknown date'

  return new Date(date).toLocaleString()
}

onMounted(() => {
  loadRequests()
})
</script>