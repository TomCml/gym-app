<template>
  <div v-if="show" class="loader-overlay">
    <img :src="plateIcon" alt="Loading..." class="spinner" />
  </div>
</template>

<script setup>
import plateIcon from '@/assets/plate_loader.webp'

defineProps({
  show: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-color: rgba(0, 0, 0, 0);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 9999;
}

.spinner {
  width: 80px;
  height: 80px;

  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
