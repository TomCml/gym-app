<!-- src/views/Home.vue (welcome screen maquette 1) -->
<template>
  <div class="home">
    <div class="header-bg">
      <img vbind :src="homePicture" alt="Woman working out" class="illustration" />
    </div>
    <h1>Welcome {{ user.username }}</h1>
    <p>Track your workouts, set goals, and stay motivated on your fitness journey.</p>
    <button class="get-started" @click="getStarted">Get Started</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'
import homePicture from '../assets/gym-app-home.webp'

const authStore = useAuthStore()

const { user } = storeToRefs(authStore)

const router = useRouter()

const getStarted = () => {
  router.push('/workouts')
}
</script>

<style scoped>
.home {
  background: var(--background-color);

  text-align: center;
  padding: 20px;
}
.header-bg {
  background: #f5a623;
  padding: 50px 0;
  margin: 0;
  margin-bottom: 20px;
}
.illustration {
  width: 400px;
}
h1 {
  font-size: 28px;
  color: #fff;
}
p {
  font-size: 16px;
  color: #888;
}
.get-started {
  background: var(--color-accent);
  color: #fff;
  padding: 15px 30px;
  border: none;
  border-radius: 30px;
  font-size: 18px;
  margin-top: 20px;
}
</style>
