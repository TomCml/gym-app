<template>
  <div class="profile">
    <h2>Profile</h2>
    <p>Username: {{ user.username }}</p>
    <p>Goal: {{ user.goal }}</p>
    <p>PR:</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'
const user = ref({})

onMounted(async () => {
  try {
    const response = await api.getCurrentUser()
    user.value = response.data
  } catch (err) {
    console.error('Error fetching profile', err)
  }
})
</script>

<style scoped>
.profile {
  padding: 20px;
  color: #fff;
}
</style>
