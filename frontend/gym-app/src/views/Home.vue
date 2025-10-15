<template>
  <div class="home">
    <div class="title">
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
      <h1>Gymbro App</h1>
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
    </div>

    <div class="header-bg">
      <img vbind :src="homePicture" alt="gym equipements" class="illustration" />
    </div>
    <h2>Welcome {{ user.username }}</h2>
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
h1 {
  font-size: 40px;
  font-family: Bungee;
  color: var(--complementary-color);
}

h2 {
  font-family: Bungee;
  font-weight: 300;
  color: var(--complementary-color);
}
.title {
  font-size: 40px;
  display: flex;
  flex-direction: row;
  align-items: center;
  color: var(--color-accent);
  gap: 8px;
}

.home {
  background: var(--background-color);

  text-align: center;
  padding: 20px;
}
.header-bg {
  background: var(--background-color);
  padding: 10px 0;
  margin: 0;
  margin-bottom: 20px;
}
.illustration {
  width: 380px;
  border: solid 2px var(--complementary-color);
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
  font-family: Quicksand;
  font-weight: 800;
  font-size: 18px;
  margin-top: 10px;
  transition: ease-in-out 0.1s;
}

.get-started:hover {
  scale: 1.05;
  transform: translateY(-2px);
}
</style>
