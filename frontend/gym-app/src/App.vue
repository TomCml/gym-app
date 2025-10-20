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
body {
  max-width: 100vw;
  max-height: 100vh;
}
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background-color: var(--color-background);
  color: #fff;
  font-family: 'Quicksand', sans-serif;
  position: relative;
}

main {
  flex-grow: 1;
  overflow-y: auto;
  position: relative;
  padding-bottom: 100px;
}
</style>
