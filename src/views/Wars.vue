<script setup>
import { ref, computed, onMounted } from 'vue'
import { getCurrentWar } from '../services/api'

const war = ref(null)
const loading = ref(true)
const error = ref(false)

/*
|--------------------------------------------------------------------------
| Fetch War
|--------------------------------------------------------------------------
*/

const fetchWar = async () => {
  loading.value = true
  error.value = false

  const result = await getCurrentWar()

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

  war.value = response.data
  loading.value = false
}

/*
|--------------------------------------------------------------------------
| Helpers
|--------------------------------------------------------------------------
*/

const warStatus = computed(() => {
  if (!war.value) return 'Unknown'

  if (war.value.state === 'warEnded') {
    return 'War Ended'
  }

  if (war.value.state === 'inWar') {
    return 'Battle Day'
  }

  if (war.value.state === 'preparation') {
    return 'Preparation Day'
  }

  return war.value.state
})

const warResult = computed(() => {
  if (!war.value?.clan || !war.value?.opponent) {
    return null
  }

  if (war.value.clan.stars > war.value.opponent.stars) {
    return 'Victory'
  }

  if (war.value.clan.stars < war.value.opponent.stars) {
    return 'Defeat'
  }

  if (
    war.value.clan.destructionPercentage >
    war.value.opponent.destructionPercentage
  ) {
    return 'Victory'
  }

  if (
    war.value.clan.destructionPercentage <
    war.value.opponent.destructionPercentage
  ) {
    return 'Defeat'
  }

  return 'Draw'
})

const resultClass = computed(() => {
  if (warResult.value === 'Victory') {
    return 'border-green-500/30 bg-green-500/10 text-green-400'
  }

  if (warResult.value === 'Defeat') {
    return 'border-red-500/30 bg-red-500/10 text-red-400'
  }

  return 'border-yellow-500/30 bg-yellow-500/10 text-yellow-400'
})

const stars = count => {
  return '★'.repeat(count || 0)
}

const attacksUsed = clan => {
  return clan?.attacks ?? 0
}

const attacksAvailable = clan => {
  if (!clan || !war.value) return 0

  const total = war.value.teamSize * war.value.attacksPerMember

  return Math.max(total - attacksUsed(clan), 0)
}

const averageStars = clan => {
  if (!clan?.members?.length) return '0.00'

  let totalStars = 0
  let totalAttacks = 0

  clan.members.forEach(member => {
    member.attacks?.forEach(attack => {
      totalStars += attack.stars || 0
      totalAttacks++
    })
  })

  if (totalAttacks === 0) return '0.00'

  return (totalStars / totalAttacks).toFixed(2)
}

/*
|--------------------------------------------------------------------------
| Sorted Members
|--------------------------------------------------------------------------
*/

const clanMembers = computed(() => {
  if (!war.value?.clan?.members) {
    return []
  }

  return [...war.value.clan.members].sort(
    (a, b) => a.mapPosition - b.mapPosition
  )
})

/*
|--------------------------------------------------------------------------
| Load
|--------------------------------------------------------------------------
*/

onMounted(() => {
  fetchWar()
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

        <div
          class="mt-2 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"
        >

          <div>
            <h1 class="text-4xl font-black sm:text-5xl">
              Clan Wars
            </h1>

            <p class="mt-4 max-w-2xl text-slate-400">
              Track our latest war performance, attacks, stars and
              destruction.
            </p>
          </div>

          <div
            v-if="war"
            class="inline-flex w-fit rounded-full border px-4 py-2 text-sm font-semibold"
            :class="resultClass"
          >
            {{ warResult }}
          </div>

        </div>

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
        class="space-y-6"
      >

        <div
          class="h-48 animate-pulse rounded-2xl border border-slate-800 bg-slate-900"
        ></div>

        <div
          class="h-32 animate-pulse rounded-2xl border border-slate-800 bg-slate-900"
        ></div>

        <div
          class="h-96 animate-pulse rounded-2xl border border-slate-800 bg-slate-900"
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
          Unable to load war data
        </h2>

        <p class="mt-2 text-sm text-red-400/80">
          Make sure the Flask backend is running and try again.
        </p>

        <button
          @click="fetchWar"
          class="mt-5 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600"
        >
          Try Again
        </button>

      </div>

      <!-- ============================================================ -->
      <!-- WAR DATA -->
      <!-- ============================================================ -->

      <template v-else-if="war">

        <!-- ========================================================== -->
        <!-- WAR STATUS -->
        <!-- ========================================================== -->

        <div
          class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >

          <div
            class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between"
          >

            <div>

              <p
                class="text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Current War
              </p>

              <h2 class="mt-1 text-2xl font-black">
                {{ warStatus }}
              </h2>

            </div>

            <div class="text-left sm:text-right">

              <p class="text-xs text-slate-600">
                War Size
              </p>

              <p class="mt-1 text-lg font-bold text-white">
                {{ war.teamSize }} vs {{ war.teamSize }}
              </p>

            </div>

          </div>

        </div>

        <!-- ========================================================== -->
        <!-- SCOREBOARD -->
        <!-- ========================================================== -->

        <div
          class="mt-6 grid grid-cols-1 gap-5 md:grid-cols-3"
        >

          <!-- COUNTING STARS -->

          <div
            class="rounded-2xl border border-blue-500/30 bg-blue-500/5 p-6"
          >

            <div class="flex items-center gap-4">

              <img
                :src="war.clan.badgeUrls.medium"
                :alt="war.clan.name"
                class="h-16 w-16 object-contain"
              />

              <div class="min-w-0">

                <p class="truncate text-lg font-bold">
                  {{ war.clan.name }}
                </p>

                <p class="mt-1 text-xs text-slate-500">
                  Level {{ war.clan.clanLevel }}
                </p>

              </div>

            </div>

            <div class="mt-6 flex items-end justify-between">

              <div>

                <p class="text-xs uppercase tracking-wider text-slate-600">
                  Stars
                </p>

                <p class="mt-1 text-5xl font-black">
                  {{ war.clan.stars }}
                </p>

              </div>

              <div class="text-right">

                <p class="text-xs text-slate-600">
                  Destruction
                </p>

                <p class="mt-1 text-xl font-bold text-blue-400">
                  {{ war.clan.destructionPercentage }}%
                </p>

              </div>

            </div>

          </div>

          <!-- VS -->

          <div
            class="flex items-center justify-center rounded-2xl border border-slate-800 bg-slate-900 p-6"
          >

            <div class="text-center">

              <div class="text-4xl font-black text-slate-700">
                VS
              </div>

              <div
                class="mt-3 inline-flex rounded-full border border-slate-700 bg-slate-950 px-3 py-1 text-xs font-semibold text-slate-500"
              >
                {{ warResult }}
              </div>

            </div>

          </div>

          <!-- OPPONENT -->

          <div
            class="rounded-2xl border border-red-500/20 bg-red-500/5 p-6"
          >

            <div class="flex items-center gap-4">

              <img
                :src="war.opponent.badgeUrls.medium"
                :alt="war.opponent.name"
                class="h-16 w-16 object-contain"
              />

              <div class="min-w-0">

                <p class="truncate text-lg font-bold">
                  {{ war.opponent.name }}
                </p>

                <p class="mt-1 text-xs text-slate-500">
                  Level {{ war.opponent.clanLevel }}
                </p>

              </div>

            </div>

            <div class="mt-6 flex items-end justify-between">

              <div>

                <p class="text-xs uppercase tracking-wider text-slate-600">
                  Stars
                </p>

                <p class="mt-1 text-5xl font-black">
                  {{ war.opponent.stars }}
                </p>

              </div>

              <div class="text-right">

                <p class="text-xs text-slate-600">
                  Destruction
                </p>

                <p class="mt-1 text-xl font-bold text-red-400">
                  {{ war.opponent.destructionPercentage }}%
                </p>

              </div>

            </div>

          </div>

        </div>

        <!-- ========================================================== -->
        <!-- WAR STATS -->
        <!-- ========================================================== -->

        <div
          class="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4"
        >

          <div
            class="rounded-xl border border-slate-800 bg-slate-900 p-5"
          >

            <p class="text-xs text-slate-600">
              Attacks Used
            </p>

            <p class="mt-2 text-2xl font-black">
              {{ attacksUsed(war.clan) }}
            </p>

          </div>

          <div
            class="rounded-xl border border-slate-800 bg-slate-900 p-5"
          >

            <p class="text-xs text-slate-600">
              Attacks Remaining
            </p>

            <p class="mt-2 text-2xl font-black">
              {{ attacksAvailable(war.clan) }}
            </p>

          </div>

          <div
            class="rounded-xl border border-slate-800 bg-slate-900 p-5"
          >

            <p class="text-xs text-slate-600">
              Average Stars
            </p>

            <p class="mt-2 text-2xl font-black">
              {{ averageStars(war.clan) }}
            </p>

          </div>

          <div
            class="rounded-xl border border-slate-800 bg-slate-900 p-5"
          >

            <p class="text-xs text-slate-600">
              Enemy Attacks
            </p>

            <p class="mt-2 text-2xl font-black">
              {{ attacksUsed(war.opponent) }}
            </p>

          </div>

        </div>

        <!-- ========================================================== -->
        <!-- MEMBER PERFORMANCE -->
        <!-- ========================================================== -->

        <div
          class="mt-8 rounded-2xl border border-slate-800 bg-slate-900"
        >

          <div
            class="border-b border-slate-800 px-6 py-5"
          >

            <h2 class="text-xl font-bold">
              Member Performance
            </h2>

            <p class="mt-1 text-sm text-slate-500">
              Individual attacks from the latest war.
            </p>

          </div>

          <div class="divide-y divide-slate-800">

            <div
              v-for="member in clanMembers"
              :key="member.tag"
              class="px-6 py-5 transition hover:bg-slate-800/30"
            >

              <div
                class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"
              >

                <!-- PLAYER -->

                <div class="flex items-center gap-4">

                  <div
                    class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg border border-slate-700 bg-slate-950 text-xs font-bold text-slate-400"
                  >
                    {{ member.mapPosition }}
                  </div>

                  <div>

                    <h3 class="font-bold">
                      {{ member.name }}
                    </h3>

                    <p class="mt-1 text-xs text-slate-600">
                      TH{{ member.townhallLevel }}
                    </p>

                  </div>

                </div>

                <!-- ATTACKS -->

                <div class="flex flex-wrap items-center gap-3">

                  <div
                    v-for="(attack, index) in member.attacks"
                    :key="index"
                    class="rounded-xl border border-slate-800 bg-slate-950 px-4 py-3"
                  >

                    <div class="flex items-center gap-3">

                      <div class="text-yellow-400">
                        {{ stars(attack.stars) }}
                      </div>

                      <div class="text-sm font-bold">
                        {{ attack.destructionPercentage }}%
                      </div>

                    </div>

                    <p class="mt-1 text-xs text-slate-600">
                      Attack {{ index + 1 }}
                    </p>

                  </div>

                  <div
                    v-if="!member.attacks?.length"
                    class="rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-600"
                  >
                    No attacks
                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </template>

    </section>

  </main>
</template>