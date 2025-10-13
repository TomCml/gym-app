<template>
  <main>
    <RouterView v-slot="{ Component }">
      <Transition name="slide-up" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>

  <BottomNav v-if="authStore.isAuthenticated" />
</template>

<script setup>
// Ton script existant
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import BottomNav from './components/BottomNav.vue'
const authStore = useAuthStore()
</script>

<style>
.app {
  max-width: 375px; /* Mobile-first, iPhone size */
  margin: 0 auto;
  background: #1e1e1e; /* Dark mode from maquettes */
  color: #fff;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}
</style>
