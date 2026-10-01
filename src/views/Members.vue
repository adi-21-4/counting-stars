<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMembers } from '../services/api'

const members = ref([])
const loading = ref(true)
const error = ref(false)

const searchQuery = ref('')
const selectedTH = ref('all')
const selectedRole = ref('all')
const sortBy = ref('rank')

/*
|--------------------------------------------------------------------------
| Fetch Members
|--------------------------------------------------------------------------
*/

const fetchMembers = async () => {
  loading.value = true
  error.value = false

  const result = await getMembers()

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

  members.value = response.data || []

  loading.value = false
}

/*
|--------------------------------------------------------------------------
| Town Hall Options
|--------------------------------------------------------------------------
*/

const townHallLevels = computed(() => {
  const levels = members.value
    .map(member => member.townHallLevel)
    .filter(level => level != null)

  return [...new Set(levels)].sort((a, b) => b - a)
})

/*
|--------------------------------------------------------------------------
| Filtered + Sorted Members
|--------------------------------------------------------------------------
*/

const filteredMembers = computed(() => {
  let result = [...members.value]

  // Search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()

    result = result.filter(member =>
      member.name?.toLowerCase().includes(query) ||
      member.tag?.toLowerCase().includes(query)
    )
  }

  // Town Hall filter
  if (selectedTH.value !== 'all') {
    result = result.filter(
      member => String(member.townHallLevel) === selectedTH.value
    )
  }

  // Role filter
  if (selectedRole.value !== 'all') {
    result = result.filter(
      member => member.role === selectedRole.value
    )
  }

  // Sorting
  result.sort((a, b) => {
    if (sortBy.value === 'rank') {
      return (a.clanRank ?? 999) - (b.clanRank ?? 999)
    }

    if (sortBy.value === 'trophies') {
      return (b.trophies ?? 0) - (a.trophies ?? 0)
    }

    if (sortBy.value === 'donations') {
      return (b.donations ?? 0) - (a.donations ?? 0)
    }

    if (sortBy.value === 'townhall') {
      return (b.townHallLevel ?? 0) - (a.townHallLevel ?? 0)
    }

    if (sortBy.value === 'name') {
      return (a.name ?? '').localeCompare(b.name ?? '')
    }

    return 0
  })

  return result
})

/*
|--------------------------------------------------------------------------
| Role Helpers
|--------------------------------------------------------------------------
*/

const roleLabel = role => {
  const roles = {
    leader: 'Leader',
    coLeader: 'Co-Leader',
    admin: 'Elder',
    member: 'Member'
  }

  return roles[role] || role
}

const roleClass = role => {
  const classes = {
    leader: 'border-yellow-500/30 bg-yellow-500/10 text-yellow-400',
    coLeader: 'border-purple-500/30 bg-purple-500/10 text-purple-400',
    admin: 'border-blue-500/30 bg-blue-500/10 text-blue-400',
    member: 'border-slate-700 bg-slate-800 text-slate-400'
  }

  return classes[role] || classes.member
}

/*
|--------------------------------------------------------------------------
| League
|--------------------------------------------------------------------------
*/

const leagueName = member => {
  return member.leagueTier?.name || member.league?.name || 'Unranked'
}

/*
|--------------------------------------------------------------------------
| Clan Rank Styling
|--------------------------------------------------------------------------
*/

const rankClass = rank => {
  if (rank === 1) {
    return 'border-2 border-yellow-400 bg-yellow-500/15 text-yellow-300'
  }

  if (rank === 2) {
    return 'border-2 border-slate-300 bg-slate-300/10 text-slate-200'
  }

  if (rank === 3) {
    return 'border-2 border-orange-400 bg-orange-500/10 text-orange-300'
  }

  return 'border border-slate-800 bg-slate-800 text-slate-400'
}

/*
|--------------------------------------------------------------------------
| Load Data
|--------------------------------------------------------------------------
*/

onMounted(() => {
  fetchMembers()
})
</script>

<template>
  <main class="min-h-screen bg-slate-950 text-white">

    <!-- ================================================================ -->
    <!-- HEADER -->
    <!-- ================================================================ -->

    <section class="border-b border-slate-800 bg-slate-950">
      <div class="mx-auto max-w-7xl px-6 py-14 lg:px-8">

        <p
          class="text-sm font-semibold uppercase tracking-wider text-blue-400"
        >
          Counting Stars
        </p>

        <h1 class="mt-2 text-4xl font-black sm:text-5xl">
          Clan Members
        </h1>

        <p class="mt-4 max-w-2xl text-slate-400">
          Meet the players fighting under the Counting Stars banner.
          Browse members, Town Hall levels, trophies and donations.
        </p>

      </div>
    </section>

    <!-- ================================================================ -->
    <!-- CONTENT -->
    <!-- ================================================================ -->

    <section class="mx-auto max-w-7xl px-6 py-10 lg:px-8">

      <!-- ============================================================ -->
      <!-- LOADING -->
      <!-- ============================================================ -->

      <div
        v-if="loading"
        class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
      >

        <div
          v-for="i in 9"
          :key="i"
          class="h-64 animate-pulse rounded-2xl border border-slate-800 bg-slate-900"
        ></div>

      </div>

      <!-- ============================================================ -->
      <!-- ERROR -->
      <!-- ============================================================ -->

      <div
        v-else-if="error"
        class="rounded-2xl border border-red-500/30 bg-red-500/10 p-6"
      >

        <h2 class="text-lg font-bold text-red-400">
          Unable to load members
        </h2>

        <p class="mt-2 text-sm text-red-400/80">
          Make sure the Flask backend is running.
        </p>

        <button
          @click="fetchMembers"
          class="mt-5 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600"
        >
          Try Again
        </button>

      </div>

      <!-- ============================================================ -->
      <!-- MAIN DATA -->
      <!-- ============================================================ -->

      <template v-else>

        <!-- ========================================================== -->
        <!-- FILTER BAR -->
        <!-- ========================================================== -->

        <div
          class="rounded-2xl border border-slate-800 bg-slate-900 p-5"
        >

          <!-- TOP FILTERS -->

          <div
            class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4"
          >

            <!-- SEARCH -->

            <div class="lg:col-span-2">

              <label
                class="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Search
              </label>

              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by player name or tag..."
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500"
              />

            </div>

            <!-- TOWN HALL -->

            <div>

              <label
                class="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Town Hall
              </label>

              <select
                v-model="selectedTH"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-blue-500"
              >

                <option value="all">
                  All Town Halls
                </option>

                <option
                  v-for="level in townHallLevels"
                  :key="level"
                  :value="String(level)"
                >
                  Town Hall {{ level }}
                </option>

              </select>

            </div>

            <!-- ROLE -->

            <div>

              <label
                class="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Role
              </label>

              <select
                v-model="selectedRole"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-blue-500"
              >

                <option value="all">
                  All Roles
                </option>

                <option value="leader">
                  Leader
                </option>

                <option value="coLeader">
                  Co-Leader
                </option>

                <option value="admin">
                  Elder
                </option>

                <option value="member">
                  Member
                </option>

              </select>

            </div>

          </div>

          <!-- SECOND FILTER ROW -->

          <div
            class="mt-4 flex flex-col gap-4 border-t border-slate-800 pt-4 sm:flex-row sm:items-center sm:justify-between"
          >

            <p class="text-sm text-slate-500">

              Showing

              <span class="font-semibold text-white">
                {{ filteredMembers.length }}
              </span>

              of

              <span class="font-semibold text-white">
                {{ members.length }}
              </span>

              members

            </p>

            <!-- SORT -->

            <div class="flex items-center gap-3">

              <label
                class="text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Sort
              </label>

              <select
                v-model="sortBy"
                class="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none focus:border-blue-500"
              >

                <option value="rank">
                  Clan Rank
                </option>

                <option value="trophies">
                  Trophies
                </option>

                <option value="donations">
                  Donations
                </option>

                <option value="townhall">
                  Town Hall
                </option>

                <option value="name">
                  Name
                </option>

              </select>

            </div>

          </div>

        </div>

        <!-- ========================================================== -->
        <!-- EMPTY STATE -->
        <!-- ========================================================== -->

        <div
          v-if="filteredMembers.length === 0"
          class="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-12 text-center"
        >

          <div class="text-5xl">
            🔍
          </div>

          <h2 class="mt-4 text-xl font-bold">
            No members found
          </h2>

          <p class="mt-2 text-sm text-slate-500">
            Try changing your search or filters.
          </p>

        </div>

        <!-- ========================================================== -->
        <!-- MEMBER GRID -->
        <!-- ========================================================== -->

        <div
          v-else
          class="mt-8 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3"
        >

          <article
            v-for="member in filteredMembers"
            :key="member.tag"
            class="group rounded-2xl border border-slate-800 bg-slate-900 p-6 transition hover:-translate-y-1 hover:border-blue-500/40 hover:bg-slate-900/90"
          >

            <!-- ====================================================== -->
            <!-- TOP -->
            <!-- ====================================================== -->

            <div class="flex items-start justify-between gap-4">

              <!-- PLAYER INFO -->

              <div class="flex min-w-0 items-center gap-4">

                <!-- TOWN HALL -->

                <div
                  class="flex h-14 w-14 flex-shrink-0 flex-col items-center justify-center rounded-xl border border-slate-700 bg-slate-950"
                >

                  <span
                    class="text-[9px] font-semibold uppercase tracking-wider text-slate-600"
                  >
                    TH
                  </span>

                  <span
                    class="text-lg font-black text-white"
                  >
                    {{ member.townHallLevel ?? '?' }}
                  </span>

                </div>

                <!-- NAME -->

                <div class="min-w-0">

                  <h2
                    class="truncate text-lg font-bold text-white"
                  >
                    {{ member.name }}
                  </h2>

                  <p
                    class="mt-1 truncate font-mono text-xs text-slate-600"
                  >
                    {{ member.tag }}
                  </p>

                </div>

              </div>

              <!-- ================================================== -->
              <!-- CLAN RANK -->
              <!-- ================================================== -->

              <div
                class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full text-xs font-bold"
                :class="rankClass(member.clanRank)"
              >
                #{{ member.clanRank }}
              </div>

            </div>

            <!-- ====================================================== -->
            <!-- ROLE -->
            <!-- ====================================================== -->

            <div class="mt-5">

              <span
                class="inline-flex rounded-full border px-3 py-1 text-xs font-semibold"
                :class="roleClass(member.role)"
              >
                {{ roleLabel(member.role) }}
              </span>

            </div>

            <!-- ====================================================== -->
            <!-- LEAGUE -->
            <!-- ====================================================== -->

            <div
              class="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-4"
            >

              <p
                class="text-xs uppercase tracking-wider text-slate-600"
              >
                League
              </p>

              <div
                class="mt-2 flex items-center gap-3"
              >

                <!-- LEAGUE ICON -->

                <div
                  class="flex h-10 w-10 flex-shrink-0 items-center justify-center"
                >

                  <img
                    v-if="member.leagueTier?.iconUrls?.small"
                    :src="member.leagueTier.iconUrls.small"
                    :alt="leagueName(member)"
                    class="h-10 w-10 object-contain"
                  />

                  <span
                    v-else
                    class="text-xl"
                  >
                    🏆
                  </span>

                </div>

                <!-- LEAGUE TEXT -->

                <div class="min-w-0">

                  <p
                    class="truncate text-sm font-semibold text-slate-300"
                  >
                    {{ leagueName(member) }}
                  </p>

                  <p
                    v-if="
                      member.league?.name &&
                      member.league.name !== 'Unranked'
                    "
                    class="mt-0.5 truncate text-xs text-slate-600"
                  >
                    {{ member.league.name }}
                  </p>

                </div>

              </div>

            </div>

            <!-- ====================================================== -->
            <!-- STATS -->
            <!-- ====================================================== -->

            <div
              class="mt-5 grid grid-cols-2 gap-3"
            >

              <!-- TROPHIES -->

              <div
                class="rounded-xl border border-slate-800 bg-slate-950 p-4"
              >

                <p class="text-xs text-slate-600">
                  Trophies
                </p>

                <p
                  class="mt-1 text-lg font-bold text-white"
                >
                  {{ member.trophies?.toLocaleString() ?? '--' }}
                </p>

              </div>

              <!-- DONATIONS -->

              <div
                class="rounded-xl border border-slate-800 bg-slate-950 p-4"
              >

                <p class="text-xs text-slate-600">
                  Donations
                </p>

                <p
                  class="mt-1 text-lg font-bold text-white"
                >
                  {{ member.donations?.toLocaleString() ?? '--' }}
                </p>

              </div>

            </div>

            <!-- ====================================================== -->
            <!-- DONATIONS RECEIVED -->
            <!-- ====================================================== -->

            <div
              class="mt-4 flex items-center justify-between text-sm"
            >

              <span class="text-slate-600">
                Donations Received
              </span>

              <span
                class="font-semibold text-slate-400"
              >
                {{ member.donationsReceived?.toLocaleString() ?? '--' }}
              </span>

            </div>

          </article>

        </div>

      </template>

    </section>

  </main>
</template>