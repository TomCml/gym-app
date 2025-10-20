<template>
  <div class="home">
    <Loader :show="dashboardStore.isLoading" />

    <div class="title">
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
      <h1>Jymbro</h1>
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
    </div>

    <div class="header-bg">
      <img :src="homePicture" alt="gym equipements" class="illustration" />
    </div>

    <div v-if="dashboardData">
      <h2>Welcome {{ user.username }}</h2>
      <div v-if="dashboardData.yesterday_skipped" class="skipped-box">
        <p>You skipped workout yesterday, that's gay</p>
      </div>
      <div class="motivation-box">
        <p>Today is</p>
        <div v-if="dashboardData.todays_workout">
          <h3>{{ dashboardData.todays_workout.name }} !</h3>
          <button class="get-started" @click="goToLiveWorkout">Let's go!</button>
        </div>
        <h3 v-else>rest day</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'
import homePicture from '../assets/gym-app-home.webp'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const router = useRouter()

const { user } = storeToRefs(authStore)
const { dashboardData } = storeToRefs(dashboardStore)

onMounted(() => {
  dashboardStore.fetchData()
})

const goToWorkouts = () => {
  router.push('/workouts')
}

const goToLiveWorkout = () => {
  router.push('/liveworkout')
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.motivation-box {
  margin-top: 20px;
  text-align: center;
}
.motivation-box p {
  color: #aaa;
  margin: 0;
}
.motivation-box h3 {
  font-family: Bungee, sans-serif;
  color: var(--color-accent);
  font-size: 24px;
  margin: 5px 0 0 0;
  font-weight: 300;
}
.skipped-box {
  margin-top: 0px;
  padding: 10px;
  border-radius: 8px;
  p {
    margin: 0;
    font-family: Bungee;
    color: var(--complementary-color);
  }
}
h1 {
  font-size: 40px;
  font-family: Bungee;
  color: var(--complementary-color);
}
h2 {
  margin: 0;
  font-family: Bungee;
  font-weight: 300;
  color: var(--complementary-color);
}
.title {
  font-size: 40px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  gap: 15px;
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
  width: 70vw;
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
  margin-top: 20px;
  transition: ease-in-out 0.1s;
}
.get-started:active {
  scale: 1.05;
}
.get-started:hover {
  scale: 1.05;
  transform: translateY(-2px);
}
</style>
