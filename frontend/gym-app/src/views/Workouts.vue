<template>
  <div>
    <Loader :show="isLoading" />

    <div class="workouts-container">
      <div class="header">
        <h2>Your Workouts</h2>
        <button @click="goToNewWorkout" class="new-workout-btn">New Workout</button>
      </div>

      <div>
        <ul v-if="workouts.length > 0 && !isLoading" class="workouts-list"></ul>
        <div v-else-if="!isLoading" class="empty-state"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useWorkoutStore } from '../stores/workout'

const router = useRouter()
const workoutStore = useWorkoutStore()

const { workouts, isLoading } = storeToRefs(workoutStore)

onMounted(() => {
  workoutStore.fetchWorkouts()
})
const goToNewWorkout = () => {
  router.push('/new-workout')
}

const goToWorkoutDetail = (workoutId) => {
  router.push(`/workouts/${workoutId}`)
}

const formatDisplayDate = (isoDate) => {
  if (!isoDate) return ''
  const date = new Date(isoDate)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<style scoped>
h2 {
  font-family: Bungee;
  font-weight: 300;
}
.workouts-container {
  padding: 20px;
  color: var(--complementary-color);
  background-color: #101922;
  max-width: 800px;
  margin: auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.new-workout-btn {
  font-family: Quicksand;
  font-weight: 600;
  background: #4a90e2;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.new-workout-btn:hover {
  background: #357abd;
}
.loading,
.empty-state {
  text-align: center;
  margin-top: 40px;
  color: #aaa;
}
.workouts-list {
  list-style: none;
  padding: 0;
}
.workouts-list li {
  background: #333;
  padding: 15px 20px;
  margin: 10px 0;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  transition:
    background-color 0.2s,
    transform 0.2s;
}
.workouts-list li:hover {
  background: #444;
  transform: translateY(-2px);
}
.workout-name {
  font-weight: bold;
}
.workout-date {
  color: #bbb;
}
</style>
