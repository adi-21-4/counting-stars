<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'



const mobileMenuOpen = ref(false)

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}


</script>

<template>
  <div class="min-h-screen bg-[#080b12] text-white">

    <!-- NAVBAR -->
    <nav class="border-b border-white/10 bg-black/30 backdrop-blur-xl">
      <div
        class="mx-auto flex max-w-7xl items-center justify-between px-6 py-5"
      >

        <!-- LOGO -->
        <RouterLink
          to="/"
          class="flex items-center gap-3"
        >

          <!-- CLAN BADGE -->
          <div
            class="flex h-11 w-11 items-center justify-center
                   rounded-xl bg-slate-900
                   shadow-lg shadow-black/30"
          >
            <img
              v-if="clan?.badgeUrls?.small"
              :src="clan.badgeUrls.small"
              alt="Counting Stars clan badge"
              class="h-10 w-10 object-contain"
            />

            <!-- Fallback while loading -->
            <span
              v-else
              class="text-2xl"
            >
              ⭐
            </span>
          </div>

          <div>
            <h1 class="font-black tracking-wide">
              COUNTING STARS
            </h1>

            <p class="text-xs text-gray-400">
              #29QCLVURL
            </p>
          </div>

        </RouterLink>


        <!-- DESKTOP NAV -->
        <div class="hidden items-center gap-8 md:flex">

          <RouterLink
            to="/"
            class="nav-link"
          >
            Home
          </RouterLink>

          <RouterLink
            to="/members"
            class="nav-link"
          >
            Members
          </RouterLink>

          <RouterLink
            to="/wars"
            class="nav-link"
          >
            Wars
          </RouterLink>

          <RouterLink
            to="/stats"
            class="nav-link"
          >
            Stats
          </RouterLink>

          <RouterLink
            to="/join"
            class="rounded-lg bg-yellow-400 px-5 py-2.5
                   font-bold text-black transition
                   hover:bg-yellow-300"
          >
            Join Us
          </RouterLink>

          <RouterLink
            to="/admin"
            class="rounded-lg border border-white/15
                   bg-white/5 px-5 py-2.5
                   font-bold text-gray-200 transition
                  hover:bg-white/10 hover:text-white"
          >
           Admin Dashboard
          </RouterLink>

        </div>

        <!-- MOBILE MENU BUTTON -->
        <button
          type="button"
          class="flex h-11 w-11 items-center justify-center rounded-xl
                 border border-white/10 bg-white/5 text-gray-200 md:hidden"
          aria-label="Toggle navigation menu"
          :aria-expanded="mobileMenuOpen"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <span v-if="!mobileMenuOpen" class="text-2xl leading-none">☰</span>
          <span v-else class="text-2xl leading-none">×</span>
        </button>

      </div>

      <!-- MOBILE NAV -->
      <div
        v-if="mobileMenuOpen"
        class="border-t border-white/10 bg-[#080b12]/95 px-4 py-4 md:hidden"
      >
        <div class="mx-auto max-w-7xl space-y-2">
          <RouterLink @click="closeMobileMenu" to="/" class="mobile-nav-link">Home</RouterLink>
          <RouterLink @click="closeMobileMenu" to="/members" class="mobile-nav-link">Members</RouterLink>
          <RouterLink @click="closeMobileMenu" to="/wars" class="mobile-nav-link">Wars</RouterLink>
          <RouterLink @click="closeMobileMenu" to="/stats" class="mobile-nav-link">Stats</RouterLink>
          <RouterLink @click="closeMobileMenu" to="/join" class="mobile-nav-link mobile-nav-join">Join Us</RouterLink>
          <RouterLink @click="closeMobileMenu" to="/admin" class="mobile-nav-link mobile-nav-admin">Admin Dashboard</RouterLink>
        </div>
      </div>
    </nav>


    <!-- PAGE CONTENT -->
    <main>
      <RouterView />
    </main>


    <!-- FOOTER -->
    <footer class="border-t border-white/10 px-6 py-8">

      <div
        class="mx-auto flex max-w-7xl flex-col
               justify-between gap-4 text-sm
               text-gray-500 sm:flex-row"
      >

        <p class="flex items-center gap-2">
          <img
            v-if="clan?.badgeUrls?.small"
            :src="clan.badgeUrls.small"
            alt=""
            class="h-6 w-6 object-contain"
          />

          <span>
            Counting Stars · #29QCLVURL
          </span>
        </p>

        <p>
          Official Clan Headquarters
        </p>

      </div>

    </footer>

  </div>
</template>


<style scoped>

.nav-link {
  color: rgb(156 163 175);
  font-size: 0.875rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: white;
}

.router-link-active.nav-link {
  color: white;
}

.mobile-nav-link {
  display: block;
  border-radius: 0.75rem;
  padding: 0.8rem 1rem;
  color: rgb(203 213 225);
  font-size: 0.95rem;
  font-weight: 600;
  transition: background-color 0.2s, color 0.2s;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background: rgb(255 255 255 / 0.06);
  color: white;
}

.mobile-nav-join {
  background: rgb(250 204 21);
  color: black;
  text-align: center;
}

.mobile-nav-join:hover,
.mobile-nav-join.router-link-active {
  background: rgb(253 224 71);
  color: black;
}

.mobile-nav-admin {
  border: 1px solid rgb(255 255 255 / 0.1);
  background: rgb(255 255 255 / 0.03);
}

</style>