<script setup>
import { ref, onMounted } from 'vue'
import {
  getClan,
  getAnnouncements
} from '../services/api'

const clan = ref(null)
const loading = ref(true)
const error = ref(false)

const announcements = ref([])
const announcementsLoading = ref(true)
const announcementsError = ref(false)

const stats = ref([
  { title: 'Clan Level', value: '--' },
  { title: 'Members', value: '-- / 50' },
  { title: 'War Wins', value: '--' },
  { title: 'Clan Points', value: '--' }
])

const fetchClan = async () => {
  loading.value = true
  error.value = false

  const result = await getClan()

  if (result.code !== 0) {
    error.value = true
    loading.value = false
    return
  }

  const response = result.data

  if (!response.success) {
    error.value = true
    loading.value = false
    return
  }

  const data = response.data

  clan.value = data

  stats.value = [
    {
      title: 'Clan Level',
      value: data.clanLevel ?? '--'
    },
    {
      title: 'Members',
      value: data.members
        ? `${data.members} / 50`
        : '-- / 50'
    },
    {
      title: 'War Wins',
      value: data.warWins ?? '--'
    },
    {
      title: 'Clan Points',
      value: data.clanPoints != null
        ? data.clanPoints.toLocaleString()
        : '--'
    }
  ]

  loading.value = false
}

const fetchAnnouncements = async () => {
  announcementsLoading.value = true
  announcementsError.value = false

  const result = await getAnnouncements()

  if (result.code !== 0) {
    announcementsError.value = true
    announcementsLoading.value = false
    return
  }

  const response = result.data

  if (!response.success) {
    announcementsError.value = true
    announcementsLoading.value = false
    return
  }

  announcements.value = response.announcements || []

  announcementsLoading.value = false
}

const formatAnnouncementDate = (dateString) => {
  if (!dateString) {
    return ''
  }

  return new Date(dateString).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const categoryClass = (category) => {
  const classes = {
    general: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    war: 'bg-red-500/10 text-red-400 border-red-500/20',
    cwl: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    recruitment: 'bg-green-500/10 text-green-400 border-green-500/20',
    event: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    important: 'bg-orange-500/10 text-orange-400 border-orange-500/20'
  }

  return classes[category] ||
    'bg-slate-800 text-slate-400 border-slate-700'
}

const categoryLabel = (category) => {
  const labels = {
    general: 'General',
    war: 'War',
    cwl: 'CWL',
    recruitment: 'Recruitment',
    event: 'Event',
    important: 'Important'
  }

  return labels[category] || 'General'
}

onMounted(() => {
  fetchClan()
  fetchAnnouncements()
})
</script>


<template>
  <main class="min-h-screen bg-slate-950 text-white">

    <!-- HERO SECTION -->
    <section
      class="relative overflow-hidden border-b border-slate-800"
    >

      <!-- Background glow -->
      <div
        class="absolute -top-40 left-1/2 h-96 w-96 -translate-x-1/2 rounded-full bg-blue-600/20 blur-3xl"
      ></div>

      <div
        class="absolute bottom-0 left-0 h-72 w-72 rounded-full bg-purple-600/10 blur-3xl"
      ></div>

      <div
        class="relative mx-auto flex max-w-7xl flex-col items-center gap-10 px-6 py-20 text-center md:flex-row md:text-left lg:px-8"
      >

        <!-- Clan Badge -->
        <div class="flex-shrink-0">
          <div
            class="flex h-40 w-40 items-center justify-center rounded-3xl border border-slate-700 bg-slate-900 p-5 shadow-2xl shadow-blue-900/20"
          >

            <img
              v-if="clan?.badgeUrls?.large"
              :src="clan.badgeUrls.large"
              alt="Counting Stars clan badge"
              class="h-full w-full object-contain"
            />

            <div
              v-else-if="loading"
              class="h-12 w-12 animate-spin rounded-full border-4 border-slate-700 border-t-blue-500"
            ></div>

            <div
              v-else
              class="text-4xl"
            >
              ⭐
            </div>

          </div>
        </div>


        <!-- Hero Content -->
        <div class="flex-1">

          <div
            class="mb-4 inline-flex items-center rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-2 text-sm font-medium text-blue-400"
          >
            <span
              class="mr-2 h-2 w-2 rounded-full bg-green-400"
            ></span>

            Clash of Clans Clan
          </div>


          <h1
            class="text-5xl font-black tracking-tight sm:text-6xl lg:text-7xl"
          >
            Counting
            <span class="text-blue-500">Stars</span>
          </h1>


          <p
            class="mt-4 max-w-2xl text-lg leading-8 text-slate-400"
          >
            Welcome to Counting Stars — a competitive Clash of Clans
            community focused on wars, Clan Games, Clan Capital and
            building a strong team together.
          </p>


          <!-- Clan Tag -->
          <div
            class="mt-6 flex flex-wrap items-center justify-center gap-3 md:justify-start"
          >

            <span class="text-sm text-slate-500">
              Clan Tag
            </span>

            <span
              class="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 font-mono text-sm text-slate-300"
            >
              #29QCLVURL
            </span>

            <span
              v-if="clan?.location?.name"
              class="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-300"
            >
              🌍 {{ clan.location.name }}
            </span>

          </div>

        </div>

      </div>
    </section>


    <!-- ERROR MESSAGE -->
    <section
      v-if="error"
      class="mx-auto max-w-7xl px-6 pt-8 lg:px-8"
    >

      <div
        class="rounded-xl border border-red-500/30 bg-red-500/10 p-5 text-red-400"
      >

        <p class="font-semibold">
          Unable to load live clan data.
        </p>

        <p class="mt-1 text-sm text-red-400/80">
          Make sure the Flask backend and Clash of Clans API are running.
        </p>

        <button
          @click="fetchClan"
          class="mt-4 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-600"
        >
          Try Again
        </button>

      </div>
    </section>


    <!-- STATS -->
    <section class="mx-auto max-w-7xl px-6 py-12 lg:px-8">

      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

        <div
          v-for="stat in stats"
          :key="stat.title"
          class="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 transition hover:border-blue-500/40 hover:bg-slate-900"
        >

          <p class="text-sm font-medium text-slate-500">
            {{ stat.title }}
          </p>

          <p
            v-if="loading"
            class="mt-3 h-9 w-24 animate-pulse rounded bg-slate-800"
          ></p>

          <p
            v-else
            class="mt-3 text-3xl font-bold text-white"
          >
            {{ stat.value }}
          </p>

        </div>

      </div>
    </section>


    <!-- ANNOUNCEMENTS -->
    <section
      v-if="!announcementsLoading && announcements.length"
      class="border-y border-slate-800 bg-slate-900/40"
    >

      <div
        class="mx-auto max-w-7xl px-6 py-16 lg:px-8"
      >

        <!-- Heading -->
        <div
          class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"
        >

          <div>

            <p
              class="text-sm font-medium text-blue-400"
            >
              CLAN NEWS
            </p>

            <h2
              class="mt-1 text-3xl font-bold"
            >
              Latest Announcements
            </h2>

            <p
              class="mt-2 text-slate-500"
            >
              Important updates and news from Counting Stars.
            </p>

          </div>

        </div>


        <!-- Announcement Cards -->
        <div
          class="mt-8 grid grid-cols-1 gap-5 lg:grid-cols-3"
        >

          <article
            v-for="announcement in announcements.slice(0, 3)"
            :key="announcement.id"
            class="group rounded-2xl border border-slate-800 bg-slate-950 p-6 transition hover:border-blue-500/40 hover:bg-slate-900"
          >

            <!-- Category + Date -->
            <div
              class="flex items-center justify-between gap-3"
            >

              <span
                :class="[
                  'rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide',
                  categoryClass(announcement.category)
                ]"
              >
                {{ categoryLabel(announcement.category) }}
              </span>

              <span
                class="text-xs text-slate-600"
              >
                {{ formatAnnouncementDate(announcement.createdAt) }}
              </span>

            </div>


            <!-- Title -->
            <h3
              class="mt-5 text-xl font-bold text-white transition group-hover:text-blue-400"
            >
              {{ announcement.title }}
            </h3>


            <!-- Content -->
            <p
              class="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-400"
            >
              {{ announcement.content }}
            </p>

          </article>

        </div>

      </div>

    </section>


    <!-- ANNOUNCEMENTS ERROR -->
    <section
      v-if="announcementsError"
      class="mx-auto max-w-7xl px-6 pt-8 lg:px-8"
    >

      <div
        class="rounded-xl border border-slate-800 bg-slate-900 p-5"
      >

        <p class="text-sm text-slate-400">
          Announcements are currently unavailable.
        </p>

      </div>

    </section>


    <!-- CLAN INFORMATION -->
    <section
      v-if="clan"
      class="mx-auto max-w-7xl px-6 pb-12 lg:px-8"
    >

      <div
        class="grid grid-cols-1 gap-6 lg:grid-cols-3"
      >

        <!-- Clan Info -->
        <div
          class="rounded-2xl border border-slate-800 bg-slate-900 p-6 lg:col-span-2"
        >

          <div class="flex items-center justify-between">

            <div>

              <p class="text-sm font-medium text-blue-400">
                ABOUT THE CLAN
              </p>

              <h2 class="mt-1 text-2xl font-bold">
                Counting Stars
              </h2>

            </div>

            <div
              v-if="clan?.warLeague?.name"
              class="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-slate-400"
            >
              {{ clan.warLeague.name }}
            </div>

          </div>


          <p
            class="mt-5 leading-7 text-slate-400"
          >
            {{ clan.description || 'No clan description available.' }}
          </p>


          <!-- Clan Labels -->
          <div
            v-if="clan.labels?.length"
            class="mt-6 flex flex-wrap gap-2"
          >

            <span
              v-for="label in clan.labels"
              :key="label.id"
              class="rounded-full border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs text-slate-400"
            >
              {{ label.name }}
            </span>

          </div>

        </div>


        <!-- Clan Capital -->
        <div
          class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >

          <p class="text-sm font-medium text-purple-400">
            CLAN CAPITAL
          </p>

          <h2 class="mt-1 text-2xl font-bold">
            Capital Hall
          </h2>

          <div class="mt-6 flex items-end gap-3">

            <span
              class="text-5xl font-black text-white"
            >
              {{ clan.capitalLeague?.name
                ? clan.capitalLeague.name
                : '--'
              }}
            </span>

          </div>

          <div class="mt-5 space-y-3">

            <div class="flex justify-between">

              <span class="text-sm text-slate-500">
                Capital Points
              </span>

              <span class="font-semibold text-white">
                {{ clan.clanCapitalPoints?.toLocaleString() ?? '--' }}
              </span>

            </div>

            <div class="flex justify-between">

              <span class="text-sm text-slate-500">
                Builder Base Points
              </span>

              <span class="font-semibold text-white">
                {{ clan.clanBuilderBasePoints?.toLocaleString() ?? '--' }}
              </span>

            </div>

          </div>

        </div>

      </div>

    </section>


    <!-- WAR CENTER -->
    <section
      class="border-y border-slate-800 bg-slate-900/40"
    >

      <div
        class="mx-auto max-w-7xl px-6 py-16 lg:px-8"
      >

        <div
          class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"
        >

          <div>

            <p class="text-sm font-medium text-red-400">
              WAR CENTER
            </p>

            <h2 class="mt-1 text-3xl font-bold">
              Battle Ready
            </h2>

            <p class="mt-2 text-slate-500">
              Follow our clan's war activity and performance.
            </p>

          </div>

          <RouterLink
            to="/wars"
            class="inline-flex items-center justify-center rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-slate-300 transition hover:border-blue-500 hover:text-blue-400"
          >
            View Wars →
          </RouterLink>

        </div>


        <div
          class="mt-8 grid grid-cols-1 gap-5 md:grid-cols-3"
        >

          <!-- War Wins -->
          <div
            class="rounded-2xl border border-slate-800 bg-slate-950 p-6"
          >

            <div class="flex items-center justify-between">

              <span class="text-sm text-slate-500">
                War Wins
              </span>

              <span class="text-2xl">
                ⚔️
              </span>

            </div>

            <p class="mt-3 text-4xl font-black">
              {{ clan?.warWins ?? '--' }}
            </p>

          </div>


          <!-- War Win Streak -->
          <div
            class="rounded-2xl border border-slate-800 bg-slate-950 p-6"
          >

            <div class="flex items-center justify-between">

              <span class="text-sm text-slate-500">
                War Win Streak
              </span>

              <span class="text-2xl">
                🔥
              </span>

            </div>

            <p class="mt-3 text-4xl font-black">
              {{ clan?.warWinStreak ?? '--' }}
            </p>

          </div>


          <!-- War League -->
          <div
            class="rounded-2xl border border-slate-800 bg-slate-950 p-6"
          >

            <div class="flex items-center justify-between">

              <span class="text-sm text-slate-500">
                War League
              </span>

              <span class="text-2xl">
                🏆
              </span>

            </div>

            <p
              class="mt-3 text-2xl font-black"
            >
              {{ clan?.warLeague?.name ?? '--' }}
            </p>

          </div>

        </div>

      </div>

    </section>


    <!-- RECRUITMENT -->
    <section
      class="mx-auto max-w-7xl px-6 py-16 lg:px-8"
    >

      <div
        class="relative overflow-hidden rounded-3xl border border-blue-500/20 bg-gradient-to-br from-blue-600/20 via-slate-900 to-purple-600/10 p-8 sm:p-12"
      >

        <div
          class="relative z-10 max-w-2xl"
        >

          <p class="text-sm font-semibold uppercase tracking-wider text-blue-400">
            Recruitment
          </p>

          <h2
            class="mt-2 text-3xl font-bold sm:text-4xl"
          >
            Ready to join Counting Stars?
          </h2>

          <p
            class="mt-4 leading-7 text-slate-400"
          >
            Looking for an active clan that participates in wars,
            Clan Games and Clan Capital? Check our requirements and
            send us your application.
          </p>

          <RouterLink
            to="/join"
            class="mt-7 inline-flex items-center rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white shadow-lg shadow-blue-900/30 transition hover:bg-blue-500"
          >
            Join the Clan

            <span class="ml-2">
              →
            </span>
          </RouterLink>

        </div>


        <!-- Decorative glow -->
        <div
          class="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-blue-500/10 blur-3xl"
        ></div>

        <div
          class="absolute -bottom-20 right-20 h-48 w-48 rounded-full bg-purple-500/10 blur-3xl"
        ></div>

      </div>

    </section>


    <!-- FOOTER INFO -->
    <section
      class="border-t border-slate-800 bg-slate-950"
    >

      <div
        class="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-8"
      >

        <p>
          Counting Stars
          <span class="text-slate-700">•</span>
          #29QCLVURL
        </p>

        <p v-if="clan?.chatLanguage?.name">
          Chat Language: {{ clan.chatLanguage.name }}
        </p>

      </div>

    </section>

  </main>
</template>