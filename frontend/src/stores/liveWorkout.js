import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'
import { useAuthStore } from './auth'

export const useLiveWorkoutStore = defineStore(
  'liveWorkout',
  () => {
    const workout = ref(null)
    const status = ref('idle')
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
        const response = await api.fetchTodaysWorkout(authStore.user.id)
        workout.value = response.data
        status.value = 'idle'
      } catch (e) {
        console.error("Failed to fetch today's workout:", e)
        if (e.response && e.response.status === 404) {
          status.value = 'idle'
        } else {
          status.value = 'error'
        }
        workout.value = null
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
        await api.createLog(authStore.user.id, setData)
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

    async function validateTodaysWorkout() {
      if (status.value === 'exercising' || status.value === 'resting') {
        return
      }

      const authStore = useAuthStore()
      let freshWorkout = null
      try {
        const response = await api.fetchTodaysWorkout(authStore.user.id)
        freshWorkout = response.data
      } catch (e) {
        console.error('No fresh workout for today or API error.', e)
      }

      const persistedWorkoutId = workout.value?.id
      const freshWorkoutId = freshWorkout?.id

      if (persistedWorkoutId !== freshWorkoutId) {
        console.log('Workout state is stale. Resetting.')
        stopWorkout()
        workout.value = freshWorkout
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
      validateTodaysWorkout,
    }
  },
  {
    persist: true,
  },
)
