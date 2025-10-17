<template>
  <div class="app">
    <main>
      <RouterView v-slot="{ Component, route }">
        <Transition :name="route.meta.transition || 'fade'" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <BottomNav v-if="authStore.isAuthenticated" />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import BottomNav from './components/BottomNav.vue'
const authStore = useAuthStore()
</script>

<style>
.app {
  max-width: 430px;
  margin: 0 auto;
  background-color: var(--color-background);
  color: #fff;
  font-family: 'Quicksand', sans-serif;
  min-height: 100vh;
  position: relative;
}

main {
  padding-bottom: 80px;
}

main {
  flex-grow: 1; /* Fait en sorte que <main> prenne toute la hauteur disponible */
  padding-bottom: 80px;
  background-color: var(--color-background); /* Assure que le fond ne "flashe" pas */
}
</style>
