<template>
  <div class="page-container">
    <Loader :show="status === 'loading'" />

    <div v-if="status === 'idle' && workout" class="content-view">
      <h2 class="subtitle">Today's Workout</h2>
      <h1 class="title">{{ workout.name }}</h1>
      <button class="btn-primary" @click="liveWorkoutStore.startWorkout()">Start Workout</button>
    </div>

    <div v-if="!workout && status === 'idle'" class="content-view">
      <p class="empty-state">No workout planned for today.</p>
      <button class="btn-secondary" @click="router.push('/workouts')">Choose a workout</button>
    </div>

    <div v-if="status === 'exercising' && currentExercise" class="content-view">
      <p class="subtitle">Set {{ currentSetIndex + 1 }} / {{ currentExercise.planned_sets }}</p>
      <h1 class="title">{{ currentExercise.exercise.name }}</h1>
      <button class="btn-primary btn-set-done" @click="handleSetDone">Set Done</button>
    </div>

    <div v-if="status === 'resting'" class="content-view">
      <div class="timer-display">{{ restTimer }}</div>
      <h1 class="title-small">Rest</h1>

      <div class="inputs-container">
        <div class="input-group">
          <label>Weight (kg)</label>
          <div class="adjustable-input">
            <button @click="adjustWeight(-5)">-5</button>
            <button @click="adjustWeight(-1)">-1</button>
            <input type="number" step="0.5" v-model.number="currentLog.weight" />
            <button @click="adjustWeight(1)">+1</button>
            <button @click="adjustWeight(5)">+5</button>
          </div>
        </div>
        <div class="input-group">
          <label>Reps</label>
          <div class="adjustable-input">
            <button @click="adjustReps(-1)">-1</button>
            <input type="number" v-model.number="currentLog.reps" />
            <button @click="adjustReps(1)">+1</button>
          </div>
        </div>
      </div>

      <p v-if="nextExercise" class="subtitle">
        Next: {{ nextExercise.exercise.name }} - Set {{ nextSetIndex + 1 }}
      </p>
    </div>

    <div v-if="status === 'finished'" class="content-view">
      <h1 class="title">Workout Complete!</h1>
      <font-awesome-icon icon="fa-solid fa-trophy" class="trophy-icon" />
      <button class="btn-primary" @click="finishAndGoHome">Finish</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useLiveWorkoutStore } from '@/stores/liveWorkout'

const router = useRouter()
const liveWorkoutStore = useLiveWorkoutStore()
const { status, workout, currentExercise, currentSetIndex, restTimer } =
  storeToRefs(liveWorkoutStore)

const currentLog = ref({ weight: 0, reps: 0 })

const nextExercise = computed(() => {
  if (!workout.value || !currentExercise.value) return null
  const setsInCurrent = currentExercise.value.planned_sets
  if (currentSetIndex.value < setsInCurrent - 1) {
    return currentExercise.value
  }
  return workout.value.workout_exercises[liveWorkoutStore.currentExerciseIndex + 1] || null
})

const nextSetIndex = computed(() => {
  if (!currentExercise.value) return 0
  const setsInCurrent = currentExercise.value.planned_sets
  return (currentSetIndex.value + 1) % setsInCurrent
})

onMounted(() => {
  if (status.value !== 'exercising' && status.value !== 'resting') {
    liveWorkoutStore.fetchTodaysWorkout()
  }
})

watch(
  [currentExercise, currentSetIndex],
  () => {
    if (currentExercise.value) {
      currentLog.value.weight = currentExercise.value.planned_weight || 0
      currentLog.value.reps = currentExercise.value.planned_reps || 0
    }
  },
  { immediate: true, deep: true },
)

watch(restTimer, (newVal) => {
  if (newVal <= 0 && status.value === 'resting') {
    handleRestFinished()
  }
})

const handleSetDone = () => {
  liveWorkoutStore.startRest()
}

const handleRestFinished = () => {
  const logData = {
    exercise_id: currentExercise.value.exercise.id,
    workout_id: workout.value.id,
    set_number: currentSetIndex.value + 1, // La série qu'on vient de finir
    reps: currentLog.value.reps,
    weight: currentLog.value.weight,
  }
  liveWorkoutStore.saveLogAndContinue(logData)
}

const adjustWeight = (amount) => {
  currentLog.value.weight = Math.max(0, currentLog.value.weight + amount)
}

const adjustReps = (amount) => {
  currentLog.value.reps = Math.max(0, currentLog.value.reps + amount)
}
const finishAndGoHome = () => {
  liveWorkoutStore.stopWorkout()
  router.push('/home')
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: calc(100vh - 120px); /* Hauteur moins header et nav */
}

.content-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.title {
  font-size: 2.5rem;
  font-family: Bungee, sans-serif;
  margin: 0;
}
.title-small {
  font-size: 1.5rem;
  font-family: Bungee, sans-serif;
  margin: 0;
}
.subtitle {
  color: #aaa;
  margin: 0;
}
.empty-state {
  font-style: italic;
  color: #888;
}

.btn-primary {
  background: var(--color-accent);
  color: #fff;
  padding: 15px 30px;
  border: none;
  border-radius: 30px;
  font-size: 18px;
  cursor: pointer;
  font-weight: bold;
  width: 80%;
  max-width: 300px;
}
.btn-set-done {
  margin-top: 40px;
}
.btn-secondary {
  background: #444;
}

.timer-display {
  font-size: 6rem;
  font-weight: bold;
  font-family: Bungee, sans-serif;
  color: var(--color-accent);
  margin: 20px 0;
}

.inputs-container {
  display: flex;
  flex-direction: column; /* Place les groupes l'un au-dessus de l'autre */
  align-items: center;
  gap: 25px;
  margin: 20px 0;
  width: 100%;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.input-group label {
  font-size: 16px;
  color: #aaa;
  font-weight: bold;
}

/* Nouveau conteneur pour l'input et ses boutons */
.adjustable-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.adjustable-input input {
  width: 80px;
  padding: 12px;
  text-align: center;
  background: #1e1e1e;
  border: 1px solid #444;
  color: #fff;
  border-radius: 8px;
  font-size: 24px;
  font-weight: bold;
  -moz-appearance: textfield;
}
.adjustable-input input::-webkit-outer-spin-button,
.adjustable-input input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.adjustable-input button {
  background-color: #444;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.adjustable-input button:hover {
  background-color: var(--color-accent);
}
</style>
