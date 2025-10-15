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
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import BottomNav from './components/BottomNav.vue'
const authStore = useAuthStore()
</script>

<style>
.app {
  max-width: 430px;
  margin: 0 auto;
  background: var(--background-color);
  color: #fff;
  font-family: 'Quicksand', sans-serif;
}
</style>
