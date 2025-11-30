<template>
  <div class="page-container">
    <Loader :show="status === 'loading'" />

    <div v-if="status === 'idle' && workout && workout.id" class="content-view">
      <h2 class="subtitle">Today's Workout</h2>
      <h1 class="title">{{ workout.name }}</h1>
      <button class="btn-primary" @click="liveWorkoutStore.startWorkout()">Start Workout</button>
    </div>

    <div v-if="!workout && status === 'idle'" class="content-view">
      <p class="subtitle">No workout planned for today.</p>
    </div>

    <div v-if="status === 'exercising' && currentExercise" class="content-view">
      <div class="header-controls">
        <button class="btn-skip" @click="skipToNext" title="Skip to next state">⏭️ Skip</button>
        <button class="btn-stop" @click="showStopModal = true" title="Stop workout">⏹️ Stop</button>
      </div>

      <p class="subtitle">Set {{ currentSetIndex + 1 }} / {{ currentExercise.planned_sets }}</p>
      <h1 class="title">{{ currentExercise.exercise.name }}</h1>
      <button class="btn-primary btn-set-done" @click="handleSetDone">Set Done</button>
    </div>

    <div v-if="status === 'resting'" class="content-view">
      <div class="header-controls">
        <button class="btn-skip" @click="skipToNext" title="Skip rest">⏭️ Skip</button>
        <button class="btn-stop" @click="showStopModal = true" title="Stop workout">⏹️ Stop</button>
      </div>

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

    <!-- Stop Workout Confirmation Modal -->
    <ConfirmationModal
      :show="showStopModal"
      title="Stop Workout"
      message="Are you sure you want to stop this workout? Your progress will be lost."
      @close="showStopModal = false"
      @confirm="handleStopWorkout"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useLiveWorkoutStore } from '@/stores/liveWorkout'
import ConfirmationModal from '@/components/ConfirmationModale.vue'

const router = useRouter()
const liveWorkoutStore = useLiveWorkoutStore()
const { status, workout, currentExercise, currentSetIndex, restTimer } =
  storeToRefs(liveWorkoutStore)

const currentLog = ref({ weight: 0, reps: 0 })
const showStopModal = ref(false)

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

const isLastSetOfExercise = computed(() => {
  if (!currentExercise.value) return false
  return currentSetIndex.value === currentExercise.value.planned_sets - 1
})

onMounted(() => {
  liveWorkoutStore.validateTodaysWorkout()
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

const skipToNext = () => {
  if (status.value === 'resting') {
    // When skipping rest, save the log and continue (same as when timer finishes)
    handleRestFinished()
  } else {
    // When skipping exercise, use store's skipToNext
    liveWorkoutStore.skipToNext()
  }
}

const nextExerciseNow = () => {
  liveWorkoutStore.nextExerciseNow()
}

const handleRestFinished = () => {
  const logData = {
    exercise_id: currentExercise.value.exercise.id,
    workout_id: workout.value.id,
    set_number: currentSetIndex.value + 1,
    reps: currentLog.value.reps,
    weight: currentLog.value.weight,
  }
  liveWorkoutStore.saveLogAndContinue(logData)
}

const handleStopWorkout = () => {
  liveWorkoutStore.stopWorkout()
  showStopModal.value = false
  router.push('/workouts')
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
  height: 100%;
}

.content-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  position: relative;
}

.header-controls {
  display: flex;
  gap: 10px;
  justify-content: center;
  width: 100%;
  margin-bottom: 10px;
}

.btn-skip,
.btn-stop {
  padding: 10px 16px;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  font-family: Quicksand, sans-serif;
}

.btn-skip {
  background: #555;
  color: #fff;
}

.btn-skip:hover {
  background: #666;
  transform: translateY(-2px);
}

.btn-stop {
  background: #d9534f;
  color: #fff;
}

.btn-stop:hover {
  background: #c9302c;
  transform: translateY(-2px);
}

.btn-next-exercise {
  background: linear-gradient(135deg, var(--color-accent), #357abd);
  color: #fff;
  padding: 15px 30px;
  border: none;
  border-radius: 30px;
  font-size: 18px;
  cursor: pointer;
  font-weight: bold;
  width: 80%;
  max-width: 300px;
  margin-top: 20px;
  transition: all 0.3s;
}

.btn-next-exercise:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4);
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
  flex-direction: column;
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
  appearance: textfield;
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
