<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Users,
  Trophy,
  Castle,
  Swords,
  Shield,
  Coins,
  Target,
  TrendingUp
} from 'lucide-vue-next'

import { getClan, getMembers, getCurrentWar } from '../services/api'

const loading = ref(true)
const error = ref('')

const clan = ref(null)
const members = ref([])
const war = ref(null)

const averageTownHall = computed(() => {
  if (!members.value.length) return 0

  const total = members.value.reduce(
    (sum, member) => sum + (member.townHallLevel || 0),
    0
  )

  return (total / members.value.length).toFixed(1)
})

const averageTrophies = computed(() => {
  if (!members.value.length) return 0

  const total = members.value.reduce(
    (sum, member) => sum + (member.trophies || 0),
    0
  )

  return Math.round(total / members.value.length)
})

const totalDonations = computed(() => {
  return members.value.reduce(
    (sum, member) => sum + (member.donations || 0),
    0
  )
})

const totalDonationsReceived = computed(() => {
  return members.value.reduce(
    (sum, member) => sum + (member.donationsReceived || 0),
    0
  )
})

const warResult = computed(() => {
  if (!war.value?.clan || !war.value?.opponent) {
    return 'N/A'
  }

  const ourStars = war.value.clan.stars || 0
  const opponentStars = war.value.opponent.stars || 0

  if (ourStars > opponentStars) return 'Victory'
  if (ourStars < opponentStars) return 'Defeat'

  const ourDestruction = war.value.clan.destructionPercentage || 0
  const opponentDestruction =
    war.value.opponent.destructionPercentage || 0

  if (ourDestruction > opponentDestruction) return 'Victory'
  if (ourDestruction < opponentDestruction) return 'Defeat'

  return 'Draw'
})

const attacksUsed = computed(() => {
  return war.value?.clan?.attacks || 0
})

const averageStarsPerAttack = computed(() => {
  const members = war.value?.clan?.members || []

  let totalAttacks = 0
  let totalAttackStars = 0

  members.forEach(member => {
    const attacks = member.attacks || []

    attacks.forEach(attack => {
      totalAttacks += 1
      totalAttackStars += attack.stars || 0
    })
  })

  if (!totalAttacks) return '0.00'

  return (totalAttackStars / totalAttacks).toFixed(2)
})

const stats = computed(() => [
  {
    title: 'Clan Level',
    value: clan.value?.clanLevel ?? '—',
    icon: Castle
  },
  {
    title: 'Members',
    value: members.value.length,
    icon: Users
  },
  {
    title: 'Clan Points',
    value: (clan.value?.clanPoints ?? 0).toLocaleString(),
    icon: Trophy
  },
  {
    title: 'Capital Points',
    value: (clan.value?.clanCapitalPoints ?? 0).toLocaleString(),
    icon: Shield
  },
  {
    title: 'Average Town Hall',
    value: averageTownHall.value,
    icon: Castle
  },
  {
    title: 'Average Trophies',
    value: averageTrophies.value.toLocaleString(),
    icon: Trophy
  },
  {
    title: 'Total Donations',
    value: totalDonations.value.toLocaleString(),
    icon: Coins
  },
  {
    title: 'Donations Received',
    value: totalDonationsReceived.value.toLocaleString(),
    icon: TrendingUp
  }
])

const fetchStats = async () => {
  loading.value = true
  error.value = ''

  try {
    const [clanResponse, membersResponse, warResponse] =
      await Promise.all([
        getClan(),
        getMembers(),
        getCurrentWar()
      ])

    if (clanResponse.code === 0) {
      clan.value = clanResponse.data?.data
    }

    if (membersResponse.code === 0) {
      members.value = membersResponse.data?.data || []
    }

    if (warResponse.code === 0) {
      war.value = warResponse.data?.data
    }

    if (
      clanResponse.code !== 0 &&
      membersResponse.code !== 0 &&
      warResponse.code !== 0
    ) {
      error.value = 'Unable to load clan statistics.'
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
    error.value = 'Unable to load clan statistics.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-white">

    <!-- Header -->
    <section class="border-b border-slate-800 bg-slate-950">
      <div class="mx-auto max-w-7xl px-6 py-12">

        <p
          class="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-yellow-400"
        >
          Counting Stars
        </p>

        <h1 class="text-4xl font-black tracking-tight md:text-5xl">
          Clan Statistics
        </h1>

        <p class="mt-4 max-w-2xl text-slate-400">
          A live overview of our clan's performance, members,
          donations, trophies and war activity.
        </p>

      </div>
    </section>

    <main class="mx-auto max-w-7xl px-6 py-10">

      <!-- Loading -->
      <div
        v-if="loading"
        class="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center"
      >
        <div
          class="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-yellow-400"
        ></div>

        <p class="text-slate-400">
          Loading clan statistics...
        </p>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="rounded-2xl border border-red-900 bg-red-950/40 p-6 text-red-300"
      >
        {{ error }}
      </div>

      <template v-else>

        <!-- Main stats -->
        <section
          class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div
            v-for="stat in stats"
            :key="stat.title"
            class="rounded-2xl border border-slate-800 bg-slate-900 p-6 transition hover:border-slate-700"
          >
            <div class="flex items-center justify-between">

              <div
                class="flex h-11 w-11 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"
              >
                <component :is="stat.icon" class="h-5 w-5" />
              </div>

            </div>

            <p class="mt-5 text-sm text-slate-400">
              {{ stat.title }}
            </p>

            <p class="mt-1 text-3xl font-black">
              {{ stat.value }}
            </p>
          </div>
        </section>

        <!-- War Statistics -->
        <section class="mt-10">

          <div class="mb-5">
            <p
              class="text-sm font-semibold uppercase tracking-widest text-yellow-400"
            >
              War Performance
            </p>

            <h2 class="mt-2 text-2xl font-bold">
              Latest War
            </h2>
          </div>

          <div
            class="grid gap-5 md:grid-cols-2 lg:grid-cols-4"
          >

            <!-- Result -->
            <div
              class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
            >
              <div class="flex items-center gap-3">
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"
                >
                  <Swords class="h-5 w-5" />
                </div>

                <span class="text-sm text-slate-400">
                  Result
                </span>
              </div>

              <p class="mt-5 text-3xl font-black">
                {{ warResult }}
              </p>
            </div>

            <!-- Stars -->
            <div
              class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
            >
              <div class="flex items-center gap-3">
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"
                >
                  <Trophy class="h-5 w-5" />
                </div>

                <span class="text-sm text-slate-400">
                  Stars
                </span>
              </div>

              <p class="mt-5 text-3xl font-black">
                {{ war?.clan?.stars ?? 0 }}
              </p>
            </div>

            <!-- Destruction -->
            <div
              class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
            >
              <div class="flex items-center gap-3">
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"
                >
                  <Target class="h-5 w-5" />
                </div>

                <span class="text-sm text-slate-400">
                  Destruction
                </span>
              </div>

              <p class="mt-5 text-3xl font-black">
                {{ war?.clan?.destructionPercentage ?? 0 }}%
              </p>
            </div>

            <!-- Average Stars -->
            <div
              class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
            >
              <div class="flex items-center gap-3">
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"
                >
                  <TrendingUp class="h-5 w-5" />
                </div>

                <span class="text-sm text-slate-400">
                  Stars / Attack
                </span>
              </div>

              <p class="mt-5 text-3xl font-black">
                {{ averageStarsPerAttack }}
              </p>
            </div>

          </div>
        </section>

        <!-- Clan information -->
        <section class="mt-10">

          <div class="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <div class="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

              <div>
                <p class="text-sm text-slate-400">
                  Clan
                </p>

                <h2 class="mt-1 text-2xl font-bold">
                  {{ clan?.name || 'Counting Stars' }}
                </h2>

                <p class="mt-1 font-mono text-sm text-slate-500">
                  {{ clan?.tag || '#29QCLVURL' }}
                </p>
              </div>

              <div class="flex flex-wrap gap-3">

                <div class="rounded-xl bg-slate-800 px-4 py-3">
                  <p class="text-xs text-slate-500">
                    Location
                  </p>

                  <p class="font-semibold">
                    {{ clan?.location?.name || 'International' }}
                  </p>
                </div>

                <div class="rounded-xl bg-slate-800 px-4 py-3">
                  <p class="text-xs text-slate-500">
                    Capital Hall
                  </p>

                  <p class="font-semibold">
                    Level {{ clan?.clanCapital?.capitalHallLevel || '—' }}
                  </p>
                </div>

                <div class="rounded-xl bg-slate-800 px-4 py-3">
                  <p class="text-xs text-slate-500">
                    Capital Points
                  </p>

                  <p class="font-semibold">
                    {{ (clan?.clanCapitalPoints ?? 0).toLocaleString() }}
                  </p>
                </div>

              </div>

            </div>

          </div>

        </section>

      </template>

    </main>
  </div>
</template>