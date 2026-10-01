<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import {
  Plus,
  Pencil,
  Trash2,
  Eye,
  EyeOff,
  Megaphone,
  X,
  Save,
  AlertCircle,
  CheckCircle
} from 'lucide-vue-next'

const API_URL = 'http://127.0.0.1:5000/api'

const announcements = ref([])
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')

const showForm = ref(false)
const editingId = ref(null)

const form = ref({
  title: '',
  content: '',
  category: 'general',
  isPublished: true
})

const categories = [
  {
    value: 'general',
    label: 'General'
  },
  {
    value: 'war',
    label: 'War'
  },
  {
    value: 'cwl',
    label: 'CWL'
  },
  {
    value: 'recruitment',
    label: 'Recruitment'
  },
  {
    value: 'event',
    label: 'Event'
  },
  {
    value: 'important',
    label: 'Important'
  }
]

const sortedAnnouncements = computed(() => {
  return [...announcements.value].sort(
    (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
  )
})

const getCategoryLabel = (category) => {
  const item = categories.find(
    (categoryItem) => categoryItem.value === category
  )

  return item ? item.label : category
}

const resetForm = () => {
  form.value = {
    title: '',
    content: '',
    category: 'general',
    isPublished: true
  }

  editingId.value = null
}

const openCreateForm = () => {
  clearMessages()
  resetForm()
  showForm.value = true
}

const openEditForm = (announcement) => {
  clearMessages()

  editingId.value = announcement.id

  form.value = {
    title: announcement.title,
    content: announcement.content,
    category: announcement.category,
    isPublished: announcement.isPublished
  }

  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  resetForm()
}

const clearMessages = () => {
  error.value = ''
  success.value = ''
}

const handleAuthError = (status) => {
  if (status === 401 || status === 422) {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')

    window.location.href = '/admin/login'

    return true
  }

  return false
}

const fetchAnnouncements = async () => {
  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('admin_token')

    const response = await axios.get(
      `${API_URL}/admin/announcements`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    announcements.value = response.data.announcements || []
  } catch (err) {
    console.error('Failed to fetch announcements:', err)

    if (handleAuthError(err.response?.status)) {
      return
    }

    error.value =
      err.response?.data?.error ||
      'Failed to load announcements.'
  } finally {
    loading.value = false
  }
}

const saveAnnouncement = async () => {
  clearMessages()

  if (!form.value.title.trim()) {
    error.value = 'Please enter an announcement title.'
    return
  }

  if (!form.value.content.trim()) {
    error.value = 'Please enter announcement content.'
    return
  }

  saving.value = true

  try {
    const token = localStorage.getItem('admin_token')

    const payload = {
      title: form.value.title.trim(),
      content: form.value.content.trim(),
      category: form.value.category,
      isPublished: form.value.isPublished
    }

    let response

    if (editingId.value) {
      response = await axios.patch(
        `${API_URL}/admin/announcements/${editingId.value}`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    } else {
      response = await axios.post(
        `${API_URL}/admin/announcements`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    }

    if (response.data.success) {
      success.value = editingId.value
        ? 'Announcement updated successfully.'
        : 'Announcement created successfully.'

      closeForm()

      await fetchAnnouncements()
    }
  } catch (err) {
    console.error('Failed to save announcement:', err)

    if (handleAuthError(err.response?.status)) {
      return
    }

    error.value =
      err.response?.data?.error ||
      'Failed to save announcement.'
  } finally {
    saving.value = false
  }
}

const togglePublished = async (announcement) => {
  clearMessages()

  try {
    const token = localStorage.getItem('admin_token')

    await axios.patch(
      `${API_URL}/admin/announcements/${announcement.id}`,
      {
        isPublished: !announcement.isPublished
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    success.value = announcement.isPublished
      ? 'Announcement unpublished.'
      : 'Announcement published.'

    await fetchAnnouncements()
  } catch (err) {
    console.error('Failed to update publication status:', err)

    if (handleAuthError(err.response?.status)) {
      return
    }

    error.value =
      err.response?.data?.error ||
      'Failed to update announcement.'
  }
}

const deleteAnnouncement = async (announcement) => {
  const confirmed = window.confirm(
    `Delete "${announcement.title}"?\n\nThis action cannot be undone.`
  )

  if (!confirmed) {
    return
  }

  clearMessages()

  try {
    const token = localStorage.getItem('admin_token')

    await axios.delete(
      `${API_URL}/admin/announcements/${announcement.id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    success.value = 'Announcement deleted successfully.'

    await fetchAnnouncements()
  } catch (err) {
    console.error('Failed to delete announcement:', err)

    if (handleAuthError(err.response?.status)) {
      return
    }

    error.value =
      err.response?.data?.error ||
      'Failed to delete announcement.'
  }
}

const formatDate = (dateString) => {
  if (!dateString) {
    return 'Unknown date'
  }

  return new Date(dateString).toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchAnnouncements()
})
</script>


<template>
  <div class="min-h-screen bg-slate-950 text-white">

    <!-- HEADER -->
    <div class="border-b border-white/10 bg-slate-900/80">
      <div
        class="mx-auto flex max-w-7xl items-center justify-between px-6 py-6"
      >
        <div>
          <div class="flex items-center gap-3">
            <div
              class="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-500/20 text-indigo-400"
            >
              <Megaphone :size="22" />
            </div>

            <div>
              <h1 class="text-2xl font-bold">
                Announcements
              </h1>

              <p class="text-sm text-slate-400">
                Manage Counting Stars clan announcements
              </p>
            </div>
          </div>
        </div>

        <button
          @click="openCreateForm"
          class="flex items-center gap-2 rounded-xl bg-indigo-500 px-4 py-3 font-semibold text-white transition hover:bg-indigo-400"
        >
          <Plus :size="18" />
          New Announcement
        </button>
      </div>
    </div>


    <!-- CONTENT -->
    <main class="mx-auto max-w-7xl px-6 py-8">

      <!-- ERROR -->
      <div
        v-if="error"
        class="mb-6 flex items-center gap-3 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-4 text-red-300"
      >
        <AlertCircle :size="20" />
        <span>{{ error }}</span>

        <button
          @click="error = ''"
          class="ml-auto text-red-300 hover:text-white"
        >
          <X :size="18" />
        </button>
      </div>


      <!-- SUCCESS -->
      <div
        v-if="success"
        class="mb-6 flex items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-4 text-emerald-300"
      >
        <CheckCircle :size="20" />
        <span>{{ success }}</span>

        <button
          @click="success = ''"
          class="ml-auto text-emerald-300 hover:text-white"
        >
          <X :size="18" />
        </button>
      </div>


      <!-- LOADING -->
      <div
        v-if="loading"
        class="flex min-h-[300px] items-center justify-center"
      >
        <div class="text-center">
          <div
            class="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-indigo-400"
          ></div>

          <p class="text-slate-400">
            Loading announcements...
          </p>
        </div>
      </div>


      <!-- EMPTY -->
      <div
        v-else-if="sortedAnnouncements.length === 0"
        class="rounded-2xl border border-white/10 bg-slate-900 p-12 text-center"
      >
        <Megaphone
          :size="42"
          class="mx-auto mb-4 text-slate-600"
        />

        <h2 class="mb-2 text-xl font-semibold">
          No announcements yet
        </h2>

        <p class="mb-6 text-slate-400">
          Create your first announcement for the clan.
        </p>

        <button
          @click="openCreateForm"
          class="rounded-xl bg-indigo-500 px-5 py-3 font-semibold hover:bg-indigo-400"
        >
          Create Announcement
        </button>
      </div>


      <!-- ANNOUNCEMENTS -->
      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="announcement in sortedAnnouncements"
          :key="announcement.id"
          class="rounded-2xl border border-white/10 bg-slate-900 p-6 shadow-xl"
        >

          <!-- TOP -->
          <div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">

            <div class="min-w-0">

              <div class="mb-3 flex flex-wrap items-center gap-2">

                <span
                  class="rounded-full bg-indigo-500/15 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-indigo-300"
                >
                  {{ getCategoryLabel(announcement.category) }}
                </span>

                <span
                  v-if="announcement.isPublished"
                  class="flex items-center gap-1 rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-300"
                >
                  <Eye :size="13" />
                  Published
                </span>

                <span
                  v-else
                  class="flex items-center gap-1 rounded-full bg-slate-700 px-3 py-1 text-xs font-semibold text-slate-300"
                >
                  <EyeOff :size="13" />
                  Draft
                </span>

              </div>

              <h2 class="text-xl font-bold text-white">
                {{ announcement.title }}
              </h2>

              <p class="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-300">
                {{ announcement.content }}
              </p>

              <p class="mt-4 text-xs text-slate-500">
                Created
                {{ formatDate(announcement.createdAt) }}
                <span v-if="announcement.createdBy">
                  · by {{ announcement.createdBy }}
                </span>
              </p>

            </div>


            <!-- ACTIONS -->
            <div class="flex shrink-0 flex-wrap gap-2">

              <button
                @click="togglePublished(announcement)"
                class="flex items-center gap-2 rounded-lg border border-white/10 bg-slate-800 px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-700"
              >
                <EyeOff
                  v-if="announcement.isPublished"
                  :size="16"
                />

                <Eye
                  v-else
                  :size="16"
                />

                {{
                  announcement.isPublished
                    ? 'Unpublish'
                    : 'Publish'
                }}
              </button>


              <button
                @click="openEditForm(announcement)"
                class="flex items-center gap-2 rounded-lg border border-white/10 bg-slate-800 px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-700"
              >
                <Pencil :size="16" />
                Edit
              </button>


              <button
                @click="deleteAnnouncement(announcement)"
                class="flex items-center gap-2 rounded-lg border border-red-500/20 bg-red-500/10 px-3 py-2 text-sm font-medium text-red-300 transition hover:bg-red-500/20"
              >
                <Trash2 :size="16" />
                Delete
              </button>

            </div>

          </div>

        </div>
      </div>

    </main>


    <!-- CREATE / EDIT MODAL -->
    <div
      v-if="showForm"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 py-6 backdrop-blur-sm"
    >

      <div
        class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-white/10 bg-slate-900 shadow-2xl"
      >

        <!-- MODAL HEADER -->
        <div
          class="flex items-center justify-between border-b border-white/10 px-6 py-5"
        >
          <div>
            <h2 class="text-xl font-bold">
              {{
                editingId
                  ? 'Edit Announcement'
                  : 'Create Announcement'
              }}
            </h2>

            <p class="mt-1 text-sm text-slate-400">
              Share important information with the clan.
            </p>
          </div>

          <button
            @click="closeForm"
            class="rounded-lg p-2 text-slate-400 hover:bg-white/5 hover:text-white"
          >
            <X :size="20" />
          </button>
        </div>


        <!-- FORM -->
        <form
          @submit.prevent="saveAnnouncement"
          class="space-y-6 p-6"
        >

          <!-- TITLE -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Title
            </label>

            <input
              v-model="form.title"
              type="text"
              maxlength="150"
              placeholder="e.g. CWL starts tomorrow!"
              class="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-400"
            />
          </div>


          <!-- CATEGORY -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Category
            </label>

            <select
              v-model="form.category"
              class="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-3 text-white outline-none focus:border-indigo-400"
            >
              <option
                v-for="category in categories"
                :key="category.value"
                :value="category.value"
              >
                {{ category.label }}
              </option>
            </select>
          </div>


          <!-- CONTENT -->
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Announcement
            </label>

            <textarea
              v-model="form.content"
              rows="7"
              maxlength="5000"
              placeholder="Write your announcement here..."
              class="w-full resize-y rounded-xl border border-white/10 bg-slate-800 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-400"
            ></textarea>

            <p class="mt-2 text-right text-xs text-slate-500">
              {{ form.content.length }}/5000
            </p>
          </div>


          <!-- PUBLISH -->
          <label
            class="flex cursor-pointer items-center gap-3 rounded-xl border border-white/10 bg-slate-800/60 p-4"
          >
            <input
              v-model="form.isPublished"
              type="checkbox"
              class="h-4 w-4 accent-indigo-500"
            />

            <div>
              <p class="font-medium text-white">
                Publish immediately
              </p>

              <p class="text-sm text-slate-400">
                Published announcements are visible on the public website.
              </p>
            </div>
          </label>


          <!-- BUTTONS -->
          <div class="flex justify-end gap-3 border-t border-white/10 pt-5">

            <button
              type="button"
              @click="closeForm"
              class="rounded-xl border border-white/10 px-5 py-3 font-medium text-slate-300 transition hover:bg-white/5"
            >
              Cancel
            </button>

            <button
              type="submit"
              :disabled="saving"
              class="flex items-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Save :size="18" />

              {{
                saving
                  ? 'Saving...'
                  : editingId
                    ? 'Save Changes'
                    : 'Create Announcement'
              }}
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>