<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Save, Settings, ShieldCheck } from 'lucide-vue-next'
import axios from 'axios'

const router = useRouter()
const API = 'http://127.0.0.1:5000/api'

const leagues = [
  'Skeleton I', 'Skeleton II', 'Skeleton III',
  'Barbarian I', 'Barbarian II', 'Barbarian III',
  'Archer I', 'Archer II', 'Archer III',
  'Wizard I', 'Wizard II', 'Wizard III',
  'Valkyrie I', 'Valkyrie II', 'Valkyrie III',
  'Witch I', 'Witch II', 'Witch III',
  'Golem I', 'Golem II', 'Golem III',
  'P.E.K.K.A I', 'P.E.K.K.A II', 'P.E.K.K.A III',
  'Titan I', 'Titan II', 'Titan III',
  'Dragon I', 'Dragon II', 'Dragon III',
  'Electro I', 'Electro II', 'Electro III',
  'Legend III', 'Legend II', 'Legend I'
]

const token = () => localStorage.getItem('admin_token')
const headers = () => ({ Authorization: `Bearer ${token()}` })

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')

const settings = ref({
  minTownHall: 15,
  minLeague: 'Skeleton I',
  minimumDonations: 1000,
  warParticipationRequired: true,
  recruitmentOpen: true,
  rules: '',
  recruitmentRequirements: ''
})

const fetchSettings = async () => {
  try {
    const response = await axios.get(`${API}/admin/clan-settings`, {
      headers: headers()
    })
    settings.value = { ...settings.value, ...(response.data.settings || {}) }
  } catch (err) {
    if (err.response?.status === 401 || err.response?.status === 422) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      router.push('/admin/login')
      return
    }
    error.value = err.response?.data?.error || 'Unable to load clan settings.'
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  saving.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await axios.patch(
      `${API}/admin/clan-settings`,
      settings.value,
      { headers: headers() }
    )

    settings.value = { ...settings.value, ...(response.data.settings || {}) }
    success.value = 'Clan settings saved successfully.'
  } catch (err) {
    error.value = err.response?.data?.error || 'Unable to save clan settings.'
  } finally {
    saving.value = false
  }
}

onMounted(fetchSettings)
</script>

<template>
  <div class="min-h-screen bg-[#080b12] text-white">
    <header class="border-b border-white/10 bg-black/20">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-8">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-400">
            Counting Stars
          </p>
          <h1 class="mt-2 text-3xl font-black">Clan Settings</h1>
          <p class="mt-2 text-slate-500">
            Manage recruitment requirements and clan rules.
          </p>
        </div>

        <button
          type="button"
          @click="router.push('/admin')"
          class="flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:border-yellow-400 hover:text-yellow-400"
        >
          <ArrowLeft class="h-4 w-4" />
          Dashboard
        </button>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-6 py-10">
      <div
        v-if="loading"
        class="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400"
      >
        Loading clan settings...
      </div>

      <div v-else class="space-y-6">
        <div
          v-if="error"
          class="rounded-xl border border-red-900 bg-red-950/40 px-5 py-4 text-sm text-red-400"
        >
          {{ error }}
        </div>

        <div
          v-if="success"
          class="rounded-xl border border-green-900 bg-green-950/40 px-5 py-4 text-sm text-green-400"
        >
          {{ success }}
        </div>

        <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div class="flex items-start gap-4">
            <div class="rounded-xl bg-yellow-400/10 p-3">
              <Settings class="h-6 w-6 text-yellow-400" />
            </div>
            <div>
              <h2 class="text-xl font-bold">Recruitment Requirements</h2>
              <p class="mt-1 text-sm text-slate-500">
                These values will be shown on the public Join Us page.
              </p>
            </div>
          </div>

          <div class="mt-8 grid gap-6 md:grid-cols-2">
            <label>
              <span class="mb-2 block text-sm font-semibold text-slate-300">
                Minimum Town Hall
              </span>
              <input
                v-model.number="settings.minTownHall"
                type="number"
                min="1"
                max="18"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-yellow-400"
              />
            </label>

            <label>
              <span class="mb-2 block text-sm font-semibold text-slate-300">
                Minimum Ranked League
              </span>
              <select
                v-model="settings.minLeague"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-yellow-400"
              >
                <option v-for="league in leagues" :key="league" :value="league">
                  {{ league }}
                </option>
              </select>
            </label>

            <label>
              <span class="mb-2 block text-sm font-semibold text-slate-300">
                Minimum Donations
              </span>
              <input
                v-model.number="settings.minimumDonations"
                type="number"
                min="0"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-yellow-400"
              />
            </label>

            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="font-semibold">War Participation</p>
                  <p class="mt-1 text-xs text-slate-500">
                    Require regular war participation.
                  </p>
                </div>

                <button
                  type="button"
                  @click="settings.warParticipationRequired = !settings.warParticipationRequired"
                  class="relative h-7 w-12 rounded-full transition"
                  :class="settings.warParticipationRequired ? 'bg-yellow-400' : 'bg-slate-700'"
                >
                  <span
                    class="absolute top-1 h-5 w-5 rounded-full bg-white transition"
                    :class="settings.warParticipationRequired ? 'left-6' : 'left-1'"
                  />
                </button>
              </div>
            </div>
          </div>

          <label class="mt-6 block">
            <span class="mb-2 block text-sm font-semibold text-slate-300">
              Recruitment Requirements
            </span>
            <textarea
              v-model="settings.recruitmentRequirements"
              rows="6"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-yellow-400"
              placeholder="Write the requirements shown to potential recruits..."
            />
          </label>
        </section>

        <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div class="flex items-start gap-4">
            <div class="rounded-xl bg-yellow-400/10 p-3">
              <ShieldCheck class="h-6 w-6 text-yellow-400" />
            </div>
            <div>
              <h2 class="text-xl font-bold">Clan Rules</h2>
              <p class="mt-1 text-sm text-slate-500">
                Rules shown publicly to recruits and clan members.
              </p>
            </div>
          </div>

          <textarea
            v-model="settings.rules"
            rows="8"
            class="mt-6 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-yellow-400"
            placeholder="Write your clan rules..."
          />
        </section>

        <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div class="flex items-center justify-between gap-6">
            <div>
              <h2 class="text-xl font-bold">Recruitment Status</h2>
              <p class="mt-1 text-sm text-slate-500">
                Turn recruitment applications on or off.
              </p>
            </div>

            <button
              type="button"
              @click="settings.recruitmentOpen = !settings.recruitmentOpen"
              class="rounded-xl border px-5 py-3 text-sm font-bold transition"
              :class="settings.recruitmentOpen
                ? 'border-green-900 bg-green-950/40 text-green-400'
                : 'border-red-900 bg-red-950/40 text-red-400'"
            >
              {{ settings.recruitmentOpen ? 'Recruitment Open' : 'Recruitment Closed' }}
            </button>
          </div>
        </section>

        <div class="flex justify-end">
          <button
            type="button"
            :disabled="saving"
            @click="saveSettings"
            class="flex items-center gap-2 rounded-xl bg-yellow-400 px-6 py-3 font-bold text-black transition hover:bg-yellow-300 disabled:opacity-50"
          >
            <Save class="h-5 w-5" />
            {{ saving ? 'Saving...' : 'Save Clan Settings' }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
