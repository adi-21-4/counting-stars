<script setup>
import { onMounted, ref } from 'vue'
import {
  ArrowLeft,
  Check,
  X,
  Clock,
  User,
  MessageCircle
} from 'lucide-vue-next'
import api from '../../services/api'

const applications = ref([])
const loading = ref(true)
const error = ref('')
const updating = ref(null)

const getToken = () => {
  return localStorage.getItem('admin_token')
}

const fetchApplications = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get(
      '/admin/applications',
      {
        headers: {
          Authorization: `Bearer ${getToken()}`
        }
      }
    )

    applications.value =
      response.data.applications || []

  } catch (err) {
    console.error(err)

    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')

      window.location.href = '/admin/login'
      return
    }

    error.value =
      err.response?.data?.error ||
      'Unable to load applications.'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (application, status) => {
  updating.value = application.id

  try {
    const response = await api.patch(
      `/admin/applications/${application.id}`,
      {
        status
      },
      {
        headers: {
          Authorization: `Bearer ${getToken()}`
        }
      }
    )

    if (response.data.success) {
      application.status = status
      application.reviewedBy =
        response.data.application.reviewedBy
    }

  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.error ||
      'Unable to update application.'
  } finally {
    updating.value = null
  }
}

const statusClass = status => {
  if (status === 'approved') {
    return 'border-green-900 bg-green-950/40 text-green-400'
  }

  if (status === 'rejected') {
    return 'border-red-900 bg-red-950/40 text-red-400'
  }

  return 'border-yellow-900 bg-yellow-950/40 text-yellow-400'
}

const statusIcon = status => {
  if (status === 'approved') return Check
  if (status === 'rejected') return X

  return Clock
}

const formatDate = date => {
  if (!date) return '—'

  return new Date(date).toLocaleString()
}

onMounted(fetchApplications)
</script>

<template>
  <div class="min-h-screen bg-[#080b12] text-white">

    <!-- Header -->
    <section class="border-b border-white/10">
      <div
        class="mx-auto max-w-7xl px-6 py-8"
      >

        <RouterLink
          to="/admin"
          class="mb-5 inline-flex items-center
                 gap-2 text-sm text-slate-500
                 transition hover:text-white"
        >
          <ArrowLeft class="h-4 w-4" />
          Back to Dashboard
        </RouterLink>

        <p
          class="text-sm font-semibold uppercase
                 tracking-[0.25em] text-yellow-400"
        >
          Admin
        </p>

        <h1 class="mt-2 text-3xl font-black">
          Recruitment Applications
        </h1>

        <p class="mt-2 text-slate-500">
          Review players who want to join Counting Stars.
        </p>

      </div>
    </section>


    <main class="mx-auto max-w-7xl px-6 py-10">

      <!-- Error -->
      <div
        v-if="error"
        class="mb-6 rounded-xl border
               border-red-900 bg-red-950/40
               px-5 py-4 text-red-300"
      >
        {{ error }}
      </div>


      <!-- Loading -->
      <div
        v-if="loading"
        class="rounded-2xl border border-slate-800
               bg-slate-900 p-10 text-center"
      >
        <div
          class="mx-auto mb-4 h-10 w-10
                 animate-spin rounded-full border-4
                 border-slate-700 border-t-yellow-400"
        ></div>

        <p class="text-slate-500">
          Loading applications...
        </p>
      </div>


      <!-- Empty -->
      <div
        v-else-if="applications.length === 0"
        class="rounded-2xl border border-slate-800
               bg-slate-900 p-12 text-center"
      >

        <User
          class="mx-auto h-12 w-12 text-slate-700"
        />

        <h2 class="mt-5 text-xl font-bold">
          No applications yet
        </h2>

        <p class="mt-2 text-slate-500">
          New recruitment applications will appear here.
        </p>

      </div>


      <!-- Applications -->
      <div
        v-else
        class="space-y-5"
      >

        <article
          v-for="application in applications"
          :key="application.id"
          class="rounded-2xl border
                 border-slate-800 bg-slate-900 p-6"
        >

          <!-- Top -->
          <div
            class="flex flex-col gap-5
                   lg:flex-row lg:items-start
                   lg:justify-between"
          >

            <div>

              <div class="flex flex-wrap items-center gap-3">

                <h2 class="text-2xl font-black">
                  {{ application.playerName }}
                </h2>

                <span
                  class="rounded-lg border px-3 py-1
                         text-xs font-bold uppercase"
                  :class="statusClass(application.status)"
                >
                  <component
                    :is="statusIcon(application.status)"
                    class="mr-1 inline h-3.5 w-3.5"
                  />

                  {{ application.status }}
                </span>

              </div>

              <p
                class="mt-1 font-mono text-sm
                       text-slate-500"
              >
                {{ application.playerTag }}
              </p>

            </div>


            <!-- Actions -->
            <div
              v-if="application.status === 'pending'"
              class="flex gap-3"
            >

              <button
                @click="updateStatus(application, 'approved')"
                :disabled="updating === application.id"
                class="flex items-center gap-2
                       rounded-xl bg-green-500/10
                       px-4 py-2.5 text-sm
                       font-bold text-green-400
                       transition hover:bg-green-500/20
                       disabled:opacity-50"
              >
                <Check class="h-4 w-4" />
                Approve
              </button>

              <button
                @click="updateStatus(application, 'rejected')"
                :disabled="updating === application.id"
                class="flex items-center gap-2
                       rounded-xl bg-red-500/10
                       px-4 py-2.5 text-sm
                       font-bold text-red-400
                       transition hover:bg-red-500/20
                       disabled:opacity-50"
              >
                <X class="h-4 w-4" />
                Reject
              </button>

            </div>

          </div>


          <!-- Player information -->
          <div
            class="mt-6 grid gap-3
                   sm:grid-cols-2 lg:grid-cols-4"
          >

            <div class="rounded-xl bg-slate-950 p-4">
              <p class="text-xs text-slate-600">
                Town Hall
              </p>

              <p class="mt-1 font-bold">
                TH{{ application.townHallLevel }}
              </p>
            </div>

            <div class="rounded-xl bg-slate-950 p-4">
              <p class="text-xs text-slate-600">
                Ranked League
              </p>

              <p class="mt-1 font-bold">
                {{ application.league || 'Not provided' }}
              </p>
            </div>

            <div class="rounded-xl bg-slate-950 p-4">
              <p class="text-xs text-slate-600">
                Age
              </p>

              <p class="mt-1 font-bold">
                {{ application.age }}
              </p>
            </div>

            <div class="rounded-xl bg-slate-950 p-4">
              <p class="text-xs text-slate-600">
                Discord
              </p>

              <p class="mt-1 truncate font-bold">
                {{ application.discord || 'Not provided' }}
              </p>
            </div>

          </div>


          <!-- Reason -->
          <div
            class="mt-5 rounded-xl border
                   border-slate-800 bg-slate-950 p-5"
          >

            <div class="flex items-center gap-2">
              <MessageCircle
                class="h-4 w-4 text-yellow-400"
              />

              <p class="text-sm font-bold">
                Why they want to join
              </p>
            </div>

            <p
              class="mt-3 whitespace-pre-line
                     text-sm leading-6 text-slate-400"
            >
              {{ application.reason }}
            </p>

          </div>


          <!-- Footer -->
          <div
            class="mt-5 flex flex-wrap gap-4
                   text-xs text-slate-600"
          >

            <span>
              Applied:
              {{ formatDate(application.createdAt) }}
            </span>

            <span
              v-if="application.reviewedBy"
            >
              Reviewed by:
              {{ application.reviewedBy }}
            </span>

          </div>

        </article>

      </div>

    </main>

  </div>
</template>