// src/stores/liveWorkout.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useLiveWorkoutStore = defineStore(
  'liveWorkout',
  () => {
    const workout = ref(null)
    const status = ref('idle') // 'idle', 'exercising', 'resting', 'finished'
    const currentExerciseIndex = ref(0)
    const currentSetIndex = ref(0)
    const restTimer = ref(0)
    let timerInterval = null

    const currentExercise = computed(
      () => workout.value?.workout_exercises[currentExerciseIndex.value],
    )

    async function fetchTodaysWorkout() {
      status.value = 'loading'
      const authStore = useAuthStore()
      try {
        const response = await axios.get(`http://localhost:8000/api/workouts/today/`, {
          params: { user_id: authStore.user.id },
        })
        workout.value = response.data
        status.value = 'idle'
      } catch (e) {
        status.value = 'error'
      }
    }

    function startWorkout() {
      currentExerciseIndex.value = 0
      currentSetIndex.value = 0
      status.value = 'exercising'
    }

    function startRest() {
      status.value = 'resting'
      restTimer.value = currentExercise.value.rest_seconds || 60

      if (timerInterval) clearInterval(timerInterval)

      timerInterval = setInterval(() => {
        restTimer.value--
        if (restTimer.value <= 0) {
          clearInterval(timerInterval)
        }
      }, 1000)
    }

    async function saveLogAndContinue(setData) {
      const authStore = useAuthStore()
      try {
        await axios.post(`http://localhost:8000/api/logs/`, setData, {
          params: { user_id: authStore.user.id },
        })
      } catch (e) {
        console.error('Failed to save log', e)
      }

      const setsInCurrentExercise = currentExercise.value.planned_sets
      if (currentSetIndex.value < setsInCurrentExercise - 1) {
        currentSetIndex.value++
      } else {
        currentExerciseIndex.value++
        currentSetIndex.value = 0
      }

      if (currentExerciseIndex.value >= workout.value.workout_exercises.length) {
        status.value = 'finished'
      } else {
        status.value = 'exercising'
      }
    }

    function stopWorkout() {
      clearInterval(timerInterval)
      workout.value = null
      status.value = 'idle'
    }

    return {
      workout,
      status,
      currentExercise,
      currentSetIndex,
      restTimer,
      fetchTodaysWorkout,
      startWorkout,
      startRest,
      saveLogAndContinue,
      stopWorkout,
    }
  },
  {
    persist: true,
  },
)
