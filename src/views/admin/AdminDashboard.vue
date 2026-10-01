<script setup>

import { computed, onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import {

  Users,

  FileText,

  Settings,

  Megaphone,

  LogOut,

  ShieldCheck,

  Clock,

  CheckCircle2,

  XCircle,

  UserPlus,

  Swords,

  ArrowRight,

  Trophy

} from 'lucide-vue-next'

import axios from 'axios'

const router = useRouter()

const user = ref({})

const applications = ref([])

const memberCount = ref(0)

const war = ref(null)

const announcements = ref([])

const loading = ref(true)

const error = ref('')

const token = () => {

  return localStorage.getItem('admin_token')

}

const authHeaders = () => ({

  Authorization: `Bearer ${token()}`

})

const pendingApplications = computed(() =>

  applications.value.filter(

    application => application.status === 'pending'

  )

)

const approvedApplications = computed(() =>

  applications.value.filter(

    application => application.status === 'approved'

  )

)

const rejectedApplications = computed(() =>

  applications.value.filter(

    application => application.status === 'rejected'

  )

)

const recentApplications = computed(() =>

  applications.value.slice(0, 5)

)

const publishedAnnouncements = computed(() =>

  announcements.value.filter(

    announcement => announcement.isPublished

  )

)

const draftAnnouncements = computed(() =>

  announcements.value.filter(

    announcement => !announcement.isPublished

  )

)

const latestAnnouncement = computed(() =>

  announcements.value.length

    ? announcements.value[0]

    : null

)

const warResult = computed(() => {

  if (!war.value?.clan || !war.value?.opponent) {

    return 'N/A'

  }

const ourStars = war.value.clan.stars || 0

  const opponentStars = war.value.opponent.stars || 0

if (ourStars > opponentStars) return 'Victory'

  if (ourStars < opponentStars) return 'Defeat'

const ourDestruction =

    war.value.clan.destructionPercentage || 0

const opponentDestruction =

    war.value.opponent.destructionPercentage || 0

if (ourDestruction > opponentDestruction) {

    return 'Victory'

  }

if (ourDestruction < opponentDestruction) {

    return 'Defeat'

  }

return 'Draw'

})

const logout = () => {

  localStorage.removeItem('admin_token')

  localStorage.removeItem('admin_user')

router.push('/admin/login')

}

const fetchDashboard = async () => {

  loading.value = true

  error.value = ''

try {

    /*

     * Get logged-in admin

     */

    const meResponse = await axios.get(

      'http://127.0.0.1:5000/api/auth/me',

      {

        headers: authHeaders()

      }

    )

user.value = meResponse.data.user

/*

     * Get applications

     */

    const applicationsResponse = await axios.get(

      'http://127.0.0.1:5000/api/admin/applications',

      {

        headers: authHeaders()

      }

    )

applications.value =

      applicationsResponse.data.applications || []

/*

     * Get clan members

     */

    const membersResponse = await axios.get(

      'http://127.0.0.1:5000/api/members'

    )

memberCount.value =

      membersResponse.data.data?.length || 0

/*

     * Get latest/current war

     */

    const warResponse = await axios.get(

      'http://127.0.0.1:5000/api/current-war'

    )

war.value = warResponse.data.data

/*
   * Get announcements
   */
  const announcementsResponse = await axios.get(
    'http://127.0.0.1:5000/api/admin/announcements',
    {
      headers: authHeaders()
    }
  )

  announcements.value =
    announcementsResponse.data.announcements || []

  } catch (err) {

    console.error('Dashboard loading failed:', err)

if (

      err.response?.status === 401 ||

      err.response?.status === 422

    ) {

      localStorage.removeItem('admin_token')

      localStorage.removeItem('admin_user')

router.push('/admin/login')

      return

    }

error.value =

      err.response?.data?.error ||

      'Unable to load dashboard.'

  } finally {

    loading.value = false

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

const formatDate = date => {

  if (!date) return '—'

return new Date(date).toLocaleString()

}

onMounted(fetchDashboard)

</script>

<template>

  <div class="min-h-screen bg-[#080b12] text-white">

<!-- HEADER -->

    <section class="border-b border-white/10 bg-black/20">

<div

        class="mx-auto flex max-w-7xl items-center

               justify-between px-6 py-8"

      >

<div>

<p

            class="text-sm font-semibold uppercase

                   tracking-[0.25em] text-yellow-400"

          >

            Counting Stars

          </p>

<h1 class="mt-2 text-3xl font-black">

            Admin Dashboard

          </h1>

<p class="mt-2 text-slate-500">

            Clan headquarters ·

            {{ user.username || 'Admin' }}

          </p>

</div>

<button

          @click="logout"

          class="flex items-center gap-2

                 rounded-xl border border-slate-700

                 px-4 py-2.5 text-sm font-semibold

                 text-slate-300 transition

                 hover:border-red-500

                 hover:text-red-400"

        >

          <LogOut class="h-4 w-4" />

          Logout

        </button>

</div>

</section>

<main class="mx-auto max-w-7xl px-6 py-10">

<!-- LOADING -->

      <div

        v-if="loading"

        class="rounded-2xl border

               border-slate-800 bg-slate-900

               p-12 text-center"

      >

<div

          class="mx-auto mb-4 h-10 w-10

                 animate-spin rounded-full border-4

                 border-slate-700

                 border-t-yellow-400"

        ></div>

<p class="text-slate-500">

          Loading dashboard...

        </p>

</div>

<!-- ERROR -->

      <div

        v-else-if="error"

        class="rounded-2xl border

               border-red-900 bg-red-950/40

               p-6 text-red-300"

      >

        {{ error }}

      </div>

<template v-else>

<!-- ADMIN IDENTITY -->

        <div

          class="mb-8 flex items-center gap-4

                 rounded-2xl border border-slate-800

                 bg-slate-900 p-6"

        >

<div

            class="flex h-12 w-12 items-center

                   justify-center rounded-xl

                   bg-yellow-400/10

                   text-yellow-400"

          >

            <ShieldCheck class="h-6 w-6" />

          </div>

<div>

<p class="font-bold">

              {{ user.username }}

            </p>

<p class="text-sm text-slate-500">

              {{

                user.role === 'co_leader'

                  ? 'Co-Leader'

                  : 'Leader'

              }}

              · Full Admin Access

            </p>

</div>

</div>

<!-- STAT CARDS -->

        <section

          class="grid gap-5 sm:grid-cols-2

                 lg:grid-cols-5"

        >

<!-- Pending -->

          <RouterLink

            to="/admin/applications"

            class="rounded-2xl border

                   border-slate-800 bg-slate-900

                   p-6 transition

                   hover:border-yellow-400/50"

          >

<div

              class="flex h-11 w-11 items-center

                     justify-center rounded-xl

                     bg-yellow-400/10

                     text-yellow-400"

            >

              <Clock class="h-5 w-5" />

            </div>

<p class="mt-5 text-sm text-slate-500">

              Pending Applications

            </p>

<p class="mt-1 text-3xl font-black">

              {{ pendingApplications.length }}

            </p>

</RouterLink>

<!-- Approved -->

          <div

            class="rounded-2xl border

                   border-slate-800 bg-slate-900

                   p-6"

          >

<div

              class="flex h-11 w-11 items-center

                     justify-center rounded-xl

                     bg-green-400/10

                     text-green-400"

            >

              <CheckCircle2 class="h-5 w-5" />

            </div>

<p class="mt-5 text-sm text-slate-500">

              Approved

            </p>

<p class="mt-1 text-3xl font-black">

              {{ approvedApplications.length }}

            </p>

</div>

<!-- Rejected -->

          <div

            class="rounded-2xl border

                   border-slate-800 bg-slate-900

                   p-6"

          >

<div

              class="flex h-11 w-11 items-center

                     justify-center rounded-xl

                     bg-red-400/10

                     text-red-400"

            >

              <XCircle class="h-5 w-5" />

            </div>

<p class="mt-5 text-sm text-slate-500">

              Rejected

            </p>

<p class="mt-1 text-3xl font-black">

              {{ rejectedApplications.length }}

            </p>

</div>

<!-- Members -->

          <div

            class="rounded-2xl border

                   border-slate-800 bg-slate-900

                   p-6"

          >

<div

              class="flex h-11 w-11 items-center

                     justify-center rounded-xl

                     bg-blue-400/10

                     text-blue-400"

            >

              <Users class="h-5 w-5" />

            </div>

<p class="mt-5 text-sm text-slate-500">

              Clan Members

            </p>

<p class="mt-1 text-3xl font-black">

              {{ memberCount }}

            </p>

</div>

<!-- Announcements -->
          <RouterLink
            to="/admin/announcements"
            class="rounded-2xl border
                   border-slate-800 bg-slate-900
                   p-6 transition
                   hover:border-yellow-400/50"
          >

            <div
              class="flex h-11 w-11 items-center
                     justify-center rounded-xl
                     bg-purple-400/10
                     text-purple-400"
            >
              <Megaphone class="h-5 w-5" />
            </div>

            <p class="mt-5 text-sm text-slate-500">
              Announcements
            </p>

            <p class="mt-1 text-3xl font-black">
              {{ announcements.length }}
            </p>

            <p class="mt-2 text-xs text-slate-600">
              {{ publishedAnnouncements.length }} published ·
              {{ draftAnnouncements.length }} drafts
            </p>

          </RouterLink>
        </section>

<!-- WAR OVERVIEW -->

        <section class="mt-10">

<div class="mb-5">

            <p

              class="text-sm font-semibold uppercase

                     tracking-widest text-yellow-400"

            >

              War Overview

            </p>

<h2 class="mt-2 text-2xl font-bold">

              Latest War

            </h2>

          </div>

<div

            class="rounded-2xl border

                   border-slate-800 bg-slate-900 p-6"

          >

<div

              class="flex flex-col gap-6

                     md:flex-row md:items-center

                     md:justify-between"

            >

<div class="flex items-center gap-5">

<div

                  class="flex h-14 w-14 items-center

                         justify-center rounded-xl

                         bg-yellow-400/10

                         text-yellow-400"

                >

                  <Swords class="h-7 w-7" />

                </div>

<div>

<p class="text-sm text-slate-500">

                    Result

                  </p>

<p class="text-2xl font-black">

                    {{ warResult }}

                  </p>

</div>

</div>

<div class="flex gap-8">

<div>

                  <p class="text-xs text-slate-600">

                    Stars

                  </p>

<p class="mt-1 text-xl font-black">

                    {{ war?.clan?.stars ?? 0 }}

                  </p>

                </div>

<div>

                  <p class="text-xs text-slate-600">

                    Destruction

                  </p>

<p class="mt-1 text-xl font-black">

                    {{ war?.clan?.destructionPercentage ?? 0 }}%

                  </p>

                </div>

<div>

                  <p class="text-xs text-slate-600">

                    Attacks

                  </p>

<p class="mt-1 text-xl font-black">

                    {{ war?.clan?.attacks ?? 0 }}

                  </p>

                </div>

</div>

<RouterLink

                to="/wars"

                class="flex items-center gap-2

                       text-sm font-bold

                       text-yellow-400

                       hover:text-yellow-300"

              >

                View War

                <ArrowRight class="h-4 w-4" />

              </RouterLink>

</div>

</div>

<!-- ANNOUNCEMENT OVERVIEW -->
        <section class="mt-10">

          <div class="mb-5 flex items-end justify-between">

            <div>
              <p
                class="text-sm font-semibold
                       uppercase tracking-widest
                       text-yellow-400"
              >
                Communications
              </p>

              <h2 class="mt-2 text-2xl font-bold">
                Announcement Overview
              </h2>
            </div>

            <RouterLink
              to="/admin/announcements"
              class="flex items-center gap-2
                     text-sm font-bold
                     text-yellow-400
                     hover:text-yellow-300"
            >
              Manage
              <ArrowRight class="h-4 w-4" />
            </RouterLink>

          </div>

          <div
            v-if="!latestAnnouncement"
            class="rounded-2xl border
                   border-slate-800 bg-slate-900
                   p-8"
          >
            <div class="flex items-center gap-4">
              <div
                class="flex h-12 w-12 items-center
                       justify-center rounded-xl
                       bg-purple-400/10
                       text-purple-400"
              >
                <Megaphone class="h-6 w-6" />
              </div>

              <div>
                <p class="font-bold">
                  No announcements yet
                </p>

                <p class="mt-1 text-sm text-slate-500">
                  Create an announcement to keep clan members informed.
                </p>
              </div>
            </div>
          </div>

          <div
            v-else
            class="rounded-2xl border
                   border-slate-800 bg-slate-900
                   p-6"
          >
            <div
              class="flex flex-col gap-5
                     md:flex-row md:items-start
                     md:justify-between"
            >

              <div class="min-w-0">

                <div class="flex flex-wrap items-center gap-3">

                  <h3 class="text-xl font-bold">
                    {{ latestAnnouncement.title }}
                  </h3>

                  <span
                    class="rounded-lg border
                           border-purple-900
                           bg-purple-950/40
                           px-2.5 py-1 text-xs
                           font-bold uppercase
                           text-purple-400"
                  >
                    {{ latestAnnouncement.category }}
                  </span>

                  <span
                    class="rounded-lg border
                           px-2.5 py-1 text-xs
                           font-bold uppercase"
                    :class="
                      latestAnnouncement.isPublished
                        ? 'border-green-900 bg-green-950/40 text-green-400'
                        : 'border-slate-700 bg-slate-800 text-slate-400'
                    "
                  >
                    {{
                      latestAnnouncement.isPublished
                        ? 'Published'
                        : 'Draft'
                    }}
                  </span>

                </div>

                <p
                  class="mt-3 whitespace-pre-line
                         text-sm leading-6 text-slate-400"
                >
                  {{ latestAnnouncement.content }}
                </p>

                <p class="mt-4 text-xs text-slate-600">
                  {{ formatDate(latestAnnouncement.createdAt) }}
                  <span
                    v-if="
                      latestAnnouncement.updatedAt &&
                      latestAnnouncement.updatedAt !==
                        latestAnnouncement.createdAt
                    "
                  >
                    · Updated {{ formatDate(latestAnnouncement.updatedAt) }}
                  </span>
                </p>

              </div>

              <RouterLink
                to="/admin/announcements"
                class="flex shrink-0 items-center gap-2
                       text-sm font-bold
                       text-yellow-400
                       hover:text-yellow-300"
              >
                Manage Announcements
                <ArrowRight class="h-4 w-4" />
              </RouterLink>

            </div>
          </div>

        </section>

        </section>

<!-- RECENT APPLICATIONS -->

        <section class="mt-10">

<div

            class="mb-5 flex items-end

                   justify-between"

          >

<div>

              <p

                class="text-sm font-semibold

                       uppercase tracking-widest

                       text-yellow-400"

              >

                Recruitment

              </p>

<h2 class="mt-2 text-2xl font-bold">

                Recent Applications

              </h2>

            </div>

<RouterLink

              to="/admin/applications"

              class="flex items-center gap-2

                     text-sm font-bold

                     text-yellow-400

                     hover:text-yellow-300"

            >

              View All

              <ArrowRight class="h-4 w-4" />

            </RouterLink>

</div>

<div

            v-if="recentApplications.length === 0"

            class="rounded-2xl border

                   border-slate-800 bg-slate-900

                   p-10 text-center"

          >

<FileText

              class="mx-auto h-10 w-10

                     text-slate-700"

            />

<p class="mt-4 text-slate-500">

              No applications yet.

            </p>

</div>

<div

            v-else

            class="overflow-hidden rounded-2xl

                   border border-slate-800

                   bg-slate-900"

          >

<div

              v-for="application in recentApplications"

              :key="application.id"

              class="flex flex-col gap-4

                     border-b border-slate-800

                     p-5 last:border-b-0

                     md:flex-row md:items-center

                     md:justify-between"

            >

<div>

<div class="flex items-center gap-3">

<p class="font-bold">

                    {{ application.playerName }}

                  </p>

<span

                    class="rounded-lg border

                           px-2.5 py-1 text-xs

                           font-bold uppercase"

                    :class="statusClass(application.status)"

                  >

                    {{ application.status }}

                  </span>

</div>

<p

                  class="mt-1 font-mono

                         text-xs text-slate-600"

                >

                  {{ application.playerTag }}

                </p>

</div>

<div

                class="flex items-center gap-5

                       text-sm text-slate-500"

              >

<span>

                  TH{{ application.townHallLevel }}

                </span>

<span>

                  {{ application.league || 'Not provided' }}

                  🏆

                </span>

<span class="hidden md:inline">

                  {{ formatDate(application.createdAt) }}

                </span>

</div>

</div>

</div>

</section>

<!-- QUICK ACTIONS -->

        <section class="mt-10">

<div class="mb-5">

<p

              class="text-sm font-semibold

                     uppercase tracking-widest

                     text-yellow-400"

            >

              Quick Actions

            </p>

<h2 class="mt-2 text-2xl font-bold">

              Manage Counting Stars

            </h2>

</div>

<div

            class="grid gap-5 md:grid-cols-2 lg:grid-cols-4"

          >

<RouterLink

              to="/admin/applications"

              class="group rounded-2xl

                     border border-slate-800

                     bg-slate-900 p-6

                     transition

                     hover:border-yellow-400/50"

            >

<FileText

                class="h-7 w-7

                       text-yellow-400"

              />

<h3

                class="mt-5 font-bold

                       group-hover:text-yellow-400"

              >

                Review Applications

              </h3>

<p

                class="mt-2 text-sm

                       text-slate-500"

              >

                Approve or reject new players.

              </p>

</RouterLink>


<RouterLink
  to="/admin/settings"
  class="group rounded-2xl
         border border-slate-800
         bg-slate-900 p-6
         transition
         hover:border-yellow-400/50"
>
  <Settings
    class="h-7 w-7
           text-yellow-400"
  />

  <h3
    class="mt-5 font-bold
           group-hover:text-yellow-400"
  >
    Clan Settings
  </h3>

  <p
    class="mt-2 text-sm
           text-slate-500"
  >
    Manage recruitment requirements and clan rules.
  </p>
</RouterLink>


<RouterLink
  to="/admin/requests"
  class="group rounded-2xl
         border border-slate-800
         bg-slate-900 p-6
         transition
         hover:border-yellow-400/50"
>
  <UserPlus
    class="h-7 w-7
           text-yellow-400"
  />

  <h3 class="mt-5 font-bold group-hover:text-yellow-400">
    Admin Requests
  </h3>

  <p class="mt-2 text-sm text-slate-500">
    Review and manage admin access requests.
  </p>
</RouterLink>

<RouterLink
              to="/admin/announcements"
              class="group rounded-2xl
                     border border-slate-800
                     bg-slate-900 p-6
                     transition
                     hover:border-yellow-400/50"
            >

              <Megaphone
                class="h-7 w-7
                       text-yellow-400"
              />

              <h3
                class="mt-5 font-bold
                       group-hover:text-yellow-400"
              >
                Manage Announcements
              </h3>

              <p
                class="mt-2 text-sm
                       text-slate-500"
              >
                Publish clan news, war updates and events.
              </p>

            </RouterLink>

          </div>

</section>

</template>

</main>

</div>

</template>
