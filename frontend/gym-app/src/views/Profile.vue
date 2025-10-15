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
import axios from 'axios'

const user = ref({})

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/users/me')
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
