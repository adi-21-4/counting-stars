<script setup>

import { onMounted, ref } from 'vue'

import api, { getClanSettings } from '../services/api'

import {

  Send,

  ShieldCheck,

  Users,

  Swords,

  Trophy,

  MessageCircle,

  CheckCircle2

} from 'lucide-vue-next'




const form = ref({

  playerName: '',

  playerTag: '',

  townHallLevel: '',

  league: '',

  age: '',

  discord: '',

  reason: ''

})

const clanSettings = ref(null)

const settingsLoading = ref(true)

const settingsError = ref('')

const submitted = ref(false)

const submitting = ref(false)

const error = ref('')

const fetchClanSettings = async () => {

  settingsLoading.value = true

  settingsError.value = ''



  const result = await getClanSettings()



  if (result.code === 0) {

    clanSettings.value = result.data?.settings || null

  } else {

    settingsError.value =

      'Unable to load current clan requirements.'

  }



  settingsLoading.value = false

}



const rankedLeagues = [
  "Skeleton 1", "Skeleton 2", "Skeleton 3",
  "Barbarian 4", "Barbarian 5", "Barbarian 6",
  "Archer 7", "Archer 8", "Archer 9",
  "Wizard 10", "Wizard 11", "Wizard 12",
  "Valkyrie 13", "Valkyrie 14", "Valkyrie 15",
  "Witch 16", "Witch 17", "Witch 18",
  "Golem 19", "Golem 20", "Golem 21",
  "P.E.K.K.A 22", "P.E.K.K.A 23", "P.E.K.K.A 24",
  "Titan 25", "Titan 26", "Titan 27",
  "Dragon 28", "Dragon 29", "Dragon 30",
  "Electro 31", "Electro 32", "Electro 33",
  "Legend 3", "Legend 2", "Legend 1"
]

const leagueRank = Object.fromEntries(
  rankedLeagues.map((league, index) => [league, index + 1])
)

const normalizeLeague = (league) =>
  String(league || "").trim().replace(/\s+/g, " ")

const isLeagueEligible = (playerLeague, minimumLeague) => {
  const playerRank = leagueRank[normalizeLeague(playerLeague)]
  const minimumRank = leagueRank[normalizeLeague(minimumLeague)]

  if (!playerRank || !minimumRank) {
    return false
  }

  return playerRank >= minimumRank
}

const submitApplication = async () => {

  error.value = ''



  if (

    !form.value.playerName ||

    !form.value.playerTag ||

    !form.value.townHallLevel ||

    !form.value.league ||

    !form.value.age ||

    !form.value.reason

  ) {

    error.value = 'Please fill in all required fields.'

    return

  }



  if (
    clanSettings.value &&
    Number(form.value.townHallLevel) < Number(clanSettings.value.minTownHall)
  ) {
    error.value =
      `Your Town Hall must be at least TH${clanSettings.value.minTownHall}.`
    return
  }

  if (
    clanSettings.value &&
    !isLeagueEligible(
      form.value.league,
      clanSettings.value.minLeague
    )
  ) {
    error.value =
      `Your Ranked League must be at least ${clanSettings.value.minLeague}.`
    return
  }

  submitting.value = true



  try {

    const response = await api.post(

      '/applications',

      form.value

    )



    if (response.data.success) {

      submitted.value = true

    }



  } catch (err) {

    console.error('Application submission failed:', err)



    error.value =

      err.response?.data?.error ||

      'Unable to submit your application. Please try again.'

  } finally {

    submitting.value = false

  }

}



const resetForm = () => {

  form.value = {

    playerName: '',

    playerTag: '',

    townHallLevel: '',

    league: '',

    age: '',

    discord: '',

    reason: ''

  }



  submitted.value = false

  error.value = ''

}

onMounted(fetchClanSettings)
</script>



<template>

  <div class="min-h-screen bg-slate-950 text-white">



    <!-- Hero -->

    <section class="border-b border-slate-800 bg-slate-950">

      <div class="mx-auto max-w-7xl px-6 py-14">



        <p

          class="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-yellow-400"

        >

          Counting Stars

        </p>



        <h1 class="text-4xl font-black tracking-tight md:text-5xl">

          Join the Clan

        </h1>



        <p class="mt-4 max-w-2xl text-lg text-slate-400">

          Looking for an active and competitive clan?

          Tell us about yourself and send an application to

          Counting Stars.

        </p>



      </div>

    </section>



    <main class="mx-auto max-w-7xl px-6 py-10">



      <!-- LIVE RECRUITMENT REQUIREMENTS -->
      <section class="mb-12">

        <div
          v-if="settingsLoading"
          class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >
          <p class="text-sm text-slate-500">
            Loading current clan requirements...
          </p>
        </div>

        <div
          v-else-if="settingsError"
          class="rounded-2xl border border-red-900 bg-red-950/40 p-5 text-sm text-red-300"
        >
          {{ settingsError }}
        </div>

        <div
          v-else-if="clanSettings"
          class="rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >
          <div class="mb-6">
            <p class="text-sm font-semibold uppercase tracking-widest text-yellow-400">
              Current Requirements
            </p>

            <h2 class="mt-2 text-2xl font-bold">
              Counting Stars Recruitment
            </h2>

            <p class="mt-2 text-sm text-slate-500">
              These requirements are managed by clan leadership.
            </p>
          </div>

          <div class="grid gap-4 sm:grid-cols-3">
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-sm text-slate-500">Minimum Town Hall</p>
              <p class="mt-1 text-2xl font-black">
                TH{{ clanSettings.minTownHall }}
              </p>
            </div>

            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-sm text-slate-500">Minimum Ranked League</p>
              <p class="mt-1 text-2xl font-black">
                {{ clanSettings.minLeague || 'Not specified' }}
              </p>
            </div>

            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-sm text-slate-500">Expected Donations</p>
              <p class="mt-1 text-2xl font-black">
                {{ Number(clanSettings.minimumDonations || 0).toLocaleString() }}
              </p>
            </div>
          </div>

          <div class="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p class="font-bold">Recruitment Requirements</p>

            <p class="mt-3 whitespace-pre-line text-sm leading-7 text-slate-400">
              {{ clanSettings.recruitmentRequirements || 'No additional requirements have been specified.' }}
            </p>
          </div>

          <div
            v-if="clanSettings.warParticipationRequired"
            class="mt-4 rounded-xl border border-yellow-900/50 bg-yellow-950/20 p-4 text-sm text-yellow-300"
          >
            ⚔️ War participation is required.
          </div>
        </div>

      </section>

      <!-- Requirements -->

      <section class="mb-12">



        <div class="mb-6">

          <p

            class="text-sm font-semibold uppercase tracking-widest text-yellow-400"

          >

            Before applying

          </p>



          <h2 class="mt-2 text-2xl font-bold">

            What we're looking for

          </h2>

        </div>



        <div class="grid gap-5 md:grid-cols-2 lg:grid-cols-4">



          <div

            class="rounded-2xl border border-slate-800 bg-slate-900 p-6"

          >

            <ShieldCheck class="h-7 w-7 text-yellow-400" />



            <h3 class="mt-4 font-bold">

              Active Players

            </h3>



            <p class="mt-2 text-sm leading-6 text-slate-400">

              Players who regularly participate in clan activities

              and keep their accounts active.

            </p>

          </div>



          <div

            class="rounded-2xl border border-slate-800 bg-slate-900 p-6"

          >

            <Swords class="h-7 w-7 text-yellow-400" />



            <h3 class="mt-4 font-bold">

              War Participation

            </h3>



            <p class="mt-2 text-sm leading-6 text-slate-400">

              Be prepared to participate in wars and use your

              attacks responsibly.

            </p>

          </div>



          <div

            class="rounded-2xl border border-slate-800 bg-slate-900 p-6"

          >

            <Users class="h-7 w-7 text-yellow-400" />



            <h3 class="mt-4 font-bold">

              Team Player

            </h3>



            <p class="mt-2 text-sm leading-6 text-slate-400">

              Respectful communication and cooperation with

              other clan members are important.

            </p>

          </div>



          <div

            class="rounded-2xl border border-slate-800 bg-slate-900 p-6"

          >

            <Trophy class="h-7 w-7 text-yellow-400" />



            <h3 class="mt-4 font-bold">

              Competitive Spirit

            </h3>



            <p class="mt-2 text-sm leading-6 text-slate-400">

              We value players who want to improve and contribute

              to the clan.

            </p>

          </div>



        </div>



      </section>



      <!-- Application -->

      <section>



        <div class="grid gap-8 lg:grid-cols-[0.8fr_1.2fr]">



          <!-- Left information -->

          <div

            class="h-fit rounded-2xl border border-slate-800 bg-slate-900 p-7"

          >



            <div

              class="flex h-12 w-12 items-center justify-center rounded-xl bg-yellow-400/10 text-yellow-400"

            >

              <MessageCircle class="h-6 w-6" />

            </div>



            <h2 class="mt-5 text-2xl font-bold">

              Recruitment Application

            </h2>



            <p class="mt-3 leading-7 text-slate-400">

              Fill out the form with your Clash of Clans details.

              Our leadership team can review your application

              before deciding whether to invite you.

            </p>



            <div class="mt-7 space-y-4">



              <div>

                <p class="text-sm text-slate-500">

                  Clan

                </p>



                <p class="mt-1 font-semibold">

                  Counting Stars

                </p>

              </div>



              <div>

                <p class="text-sm text-slate-500">

                  Clan Tag

                </p>



                <p class="mt-1 font-mono font-semibold">

                  #29QCLVURL

                </p>

              </div>



              <div>

                <p class="text-sm text-slate-500">

                  Application

                </p>



                <p class="mt-1 font-semibold">

                  Reviewed by Clan Leadership

                </p>

              </div>



            </div>



          </div>



          <!-- Form -->

          <div

            class="rounded-2xl border border-slate-800 bg-slate-900 p-7"

          >



            <!-- Recruitment Closed -->
            <div
              v-if="!settingsLoading && clanSettings && !clanSettings.recruitmentOpen"
              class="flex min-h-[500px] flex-col items-center justify-center text-center"
            >
              <div
                class="flex h-20 w-20 items-center justify-center rounded-full bg-red-500/10 text-red-400"
              >
                🔒
              </div>

              <h2 class="mt-6 text-3xl font-black">
                Recruitment is currently closed
              </h2>

              <p class="mt-3 max-w-md text-slate-400">
                Counting Stars is not accepting new applications right now.
                Please check back later.
              </p>
            </div>

            <!-- Success -->

            <div

              v-else-if="submitted"

              class="flex min-h-[500px] flex-col items-center justify-center text-center"

            >



              <div

                class="flex h-20 w-20 items-center justify-center rounded-full bg-green-500/10 text-green-400"

              >

                <CheckCircle2 class="h-10 w-10" />

              </div>



              <h2 class="mt-6 text-3xl font-black">

                Application Submitted

              </h2>



              <p class="mt-3 max-w-md text-slate-400">

                Thanks for applying to Counting Stars.

                Your application has been received by the clan

                leadership team.

              </p>



              <button

                type="button"

                @click="resetForm"

                class="mt-7 rounded-xl bg-yellow-400 px-6 py-3 font-bold text-slate-950 transition hover:bg-yellow-300"

              >

                Submit Another Application

              </button>



            </div>



            <!-- Form -->

            <form

              v-else

              @submit.prevent="submitApplication"

              class="space-y-6"

            >



              <div>

                <h2 class="text-2xl font-bold">

                  Player Details

                </h2>



                <p class="mt-1 text-sm text-slate-500">

                  Fields marked with * are required.

                </p>

              </div>



              <!-- Name + Tag -->

              <div class="grid gap-5 md:grid-cols-2">



                <div>

                  <label class="mb-2 block text-sm font-medium">

                    Player Name *

                  </label>



                  <input

                    v-model="form.playerName"

                    type="text"

                    placeholder="e.g. Athena"

                    class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-yellow-400"

                  />

                </div>



                <div>

                  <label class="mb-2 block text-sm font-medium">

                    Player Tag *

                  </label>



                  <input

                    v-model="form.playerTag"

                    type="text"

                    placeholder="e.g. #ABC123"

                    class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 font-mono text-white outline-none transition placeholder:text-slate-600 focus:border-yellow-400"

                  />

                </div>



              </div>



              <!-- TH + Ranked League + Age -->

              <div class="grid gap-5 md:grid-cols-3">



                <div>

                  <label class="mb-2 block text-sm font-medium">

                    Town Hall *

                  </label>



                  <select

                    v-model="form.townHallLevel"

                    class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-yellow-400"

                  >

                    <option value="">

                      Select TH

                    </option>



                    <option

                      v-for="level in 18"

                      :key="level"

                      :value="level"

                    >

                      TH{{ level }}

                    </option>

                  </select>

                </div>



                <div>
              <label
                class="mb-2 block text-sm font-medium"
              >
                Current Ranked League *
              </label>

              <select
                v-model="form.league"
                class="w-full rounded-xl border border-slate-700
                       bg-slate-950 px-4 py-3 text-white
                       outline-none focus:border-yellow-400"
              >
                <option value="">Select League</option>
                <option value="Skeleton 1">Skeleton 1</option>
                <option value="Skeleton 2">Skeleton 2</option>
                <option value="Skeleton 3">Skeleton 3</option>
                <option value="Barbarian 4">Barbarian 4</option>
                <option value="Barbarian 5">Barbarian 5</option>
                <option value="Barbarian 6">Barbarian 6</option>
                <option value="Archer 7">Archer 7</option>
                <option value="Archer 8">Archer 8</option>
                <option value="Archer 9">Archer 9</option>
                <option value="Wizard 10">Wizard 10</option>
                <option value="Wizard 11">Wizard 11</option>
                <option value="Wizard 12">Wizard 12</option>
                <option value="Valkyrie 13">Valkyrie 13</option>
                <option value="Valkyrie 14">Valkyrie 14</option>
                <option value="Valkyrie 15">Valkyrie 15</option>
                <option value="Witch 16">Witch 16</option>
                <option value="Witch 17">Witch 17</option>
                <option value="Witch 18">Witch 18</option>
                <option value="Golem 19">Golem 19</option>
                <option value="Golem 20">Golem 20</option>
                <option value="Golem 21">Golem 21</option>
                <option value="P.E.K.K.A 22">P.E.K.K.A 22</option>
                <option value="P.E.K.K.A 23">P.E.K.K.A 23</option>
                <option value="P.E.K.K.A 24">P.E.K.K.A 24</option>
                <option value="Titan 25">Titan 25</option>
                <option value="Titan 26">Titan 26</option>
                <option value="Titan 27">Titan 27</option>
                <option value="Dragon 28">Dragon 28</option>
                <option value="Dragon 29">Dragon 29</option>
                <option value="Dragon 30">Dragon 30</option>
                <option value="Electro 31">Electro 31</option>
                <option value="Electro 32">Electro 32</option>
                <option value="Electro 33">Electro 33</option>
                <option value="Legend 3">Legend 3</option>
                <option value="Legend 2">Legend 2</option>
                <option value="Legend 1">Legend 1</option>
              </select>
            </div>



                <div>

                  <label class="mb-2 block text-sm font-medium">

                    Age *

                  </label>



                  <input

                    v-model="form.age"

                    type="number"

                    min="13"

                    placeholder="Age"

                    class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-yellow-400"

                  />

                </div>



              </div>



              <!-- Discord -->

              <div>

                <label class="mb-2 block text-sm font-medium">

                  Discord Username

                </label>



                <input

                  v-model="form.discord"

                  type="text"

                  placeholder="e.g. player123"

                  class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-yellow-400"

                />

              </div>



              <!-- Reason -->

              <div>

                <label class="mb-2 block text-sm font-medium">

                  Why do you want to join? *

                </label>



                <textarea

                  v-model="form.reason"

                  rows="5"

                  placeholder="Tell us a little about yourself, your war experience and why you want to join..."

                  class="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-yellow-400"

                ></textarea>

              </div>



              <!-- Error -->

              <div

                v-if="error"

                class="rounded-xl border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300"

              >

                {{ error }}

              </div>



              <!-- Submit -->

              <button

                type="submit"

                :disabled="submitting"

                class="flex w-full items-center justify-center gap-2 rounded-xl bg-yellow-400 px-6 py-3.5 font-bold text-slate-950 transition hover:bg-yellow-300 disabled:cursor-not-allowed disabled:opacity-60"

              >

                <Send class="h-5 w-5" />



                {{

                  submitting

                    ? 'Submitting...'

                    : 'Submit Application'

                }}

              </button>



            </form>



          </div>



        </div>



      </section>



    </main>

  </div>

</template>