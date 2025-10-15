<template>
  <div>
    <Loader :show="isLoading" />

    <div class="workouts-container">
      <div class="header">
        <h2>Your Workouts</h2>
        <button @click="goToNewWorkout" class="new-workout-btn">+</button>
      </div>

      <div>
        <ul v-if="workouts.length > 0 && !isLoading" class="workouts-list">
          <li v-for="workout in workouts" :key="workout.id" @click="goToWorkoutEdit(workout.id)">
            <div>
              <div class="workout-name">{{ workout.name }}</div>

              <div v-if="workout.workout_exercises.length" class="workout-exercises">
                {{ workout.workout_exercises.map((we) => we.exercise.name).join(', ') }}
              </div>
            </div>
            <div class="workout-date">{{ formatDisplayDate(workout.date) }}</div>
          </li>
        </ul>

        <div v-else-if="!isLoading" class="empty-state">
          <p>You don't have any workouts yet.</p>
          <p>Click "+" to get started!</p>
        </div>
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

const goToWorkoutEdit = (workoutId) => {
  // On pointe vers la route d'édition qu'on a créée
  router.push(`/workouts/edit/${workoutId}`)
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
  font-size: 24px;
  background: #4a90e2;
  color: #fff;
  padding: 10px 18px;
  border: none;
  border-radius: 60px;
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
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #333;
  padding: 15px 20px;
  margin: 10px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: ease-in-out 0.1s;
}
.workouts-list li:hover {
  background: #444;
  transform: translateY(-2px);
  scale: 1.05;
}
.workout-name {
  font-weight: bold;
  margin-bottom: 5px;
}
.workout-date {
  color: #bbb;
}

.workout-exercises {
  font-size: 13px;
  color: #aaa;
  font-style: italic;
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.workout-date {
  color: #bbb;
  flex-shrink: 0;
  margin-left: 10px;
}
</style>
