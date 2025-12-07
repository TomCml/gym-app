import { defineStore } from 'pinia'
import { api } from '@/services/api'
import { useAuthStore } from './auth'

export const useLiveWorkoutStore = defineStore('liveWorkout', {
  state: () => ({
    workout: null,
    status: 'idle',
    currentExerciseIndex: 0,
    currentSetIndex: 0,
    restTimer: 0,
    timerInterval: null,
    logs: [],
  }),
  persist: true,
  actions: {
    async fetchTodaysWorkout() {
      this.status = 'loading'
      const authStore = useAuthStore()
      try {
        const response = await api.fetchTodaysWorkout(authStore.user.id)
        this.workout = response.data
        this.status = 'idle'
      } catch (e) {
        console.error("Failed to fetch today's workout:", e)
        if (e.response && e.response.status === 404) {
          this.status = 'idle'
        } else {
          this.status = 'error'
        }
        this.workout = null
      }
    },

    startWorkout() {
      this.currentExerciseIndex = 0
      this.currentSetIndex = 0
      this.status = 'exercising'
    },

    startRest() {
      this.status = 'resting'
      this.restTimer = this.currentExercise.rest_seconds || 60

      if (this.timerInterval) clearInterval(this.timerInterval)

      this.timerInterval = setInterval(() => {
        this.restTimer--
        if (this.restTimer <= 0) {
          clearInterval(this.timerInterval)
        }
      }, 1000)
    },

    resumeRest() {
      if (this.timerInterval) clearInterval(this.timerInterval)

      this.timerInterval = setInterval(() => {
        this.restTimer--
        if (this.restTimer <= 0) {
          clearInterval(this.timerInterval)
        }
      }, 1000)
    },

    async saveLogAndContinue(setData) {
      this.logs.push(setData)

      const authStore = useAuthStore()
      try {
        await api.createLog(authStore.user.id, setData)
        const idx = this.logs.findIndex(
          (l) =>
            l.exercise_id === setData.exercise_id &&
            l.workout_id === setData.workout_id &&
            l.set_number === setData.set_number,
        )
        if (idx !== -1) this.logs.splice(idx, 1)
      } catch (e) {
        console.error('Failed to send single log, kept in backlog', e)
      }

      const setsInCurrentExercise = this.currentExercise.planned_sets
      if (this.currentSetIndex < setsInCurrentExercise - 1) {
        this.currentSetIndex++
      } else {
        this.currentExerciseIndex++
        this.currentSetIndex = 0
      }

      if (this.currentExerciseIndex >= this.workout.workout_exercises.length) {
        this.status = 'finished'
      } else {
        this.status = 'exercising'
      }
    },

    stopWorkout() {
      if (this.timerInterval) clearInterval(this.timerInterval)
      this.workout = null
      this.status = 'idle'
      this.currentExerciseIndex = 0
      this.currentSetIndex = 0
      this.restTimer = 0
      this.logs = []
    },

    async flushLogs() {
      if (!this.logs.length) return
      const toSend = [...this.logs]
      try {
        await api.addLogsToWorkout(toSend)
        this.logs = []
      } catch (e) {
        console.error('Failed to flush logs batch', e)
      }
    },

    skipToNext() {
      if (this.status === 'resting') {
        if (this.timerInterval) {
          clearInterval(this.timerInterval)
          this.timerInterval = null
        }
        this.restTimer = 0
        this.status = 'exercising'
      } else if (this.status === 'exercising') {
        const setData = {
          exercise_id: this.currentExercise.exercise.id,
          workout_id: this.workout.id,
          set_number: this.currentSetIndex + 1,
          reps: 0,
          weight: 0,
        }
        this.saveLogAndContinue(setData)
      }
    },

    nextExerciseNow() {
      if (this.currentExerciseIndex < this.workout.workout_exercises.length - 1) {
        this.currentExerciseIndex++
        this.currentSetIndex = 0
        this.status = 'exercising'
      } else {
        this.status = 'finished'
      }
    },

    async validateTodaysWorkout() {
      const authStore = useAuthStore()
      if (!authStore.user?.id) {
        this.status = 'idle'
        this.workout = null
        return
      }

      if (this.workout && (this.status === 'exercising' || this.status === 'resting')) {
        console.log('Workout en cours détecté, on ne réinitialise pas le state.')
        return
      }

      let freshWorkout = null
      try {
        const response = await api.fetchTodaysWorkout(authStore.user.id)
        freshWorkout = response.data
      } catch (e) {
        console.error('Error fetching today workout:', e)
        if (this.status !== 'exercising' && this.status !== 'resting') {
          this.status = 'idle'
          this.workout = null
        }
        return
      }

      if (freshWorkout && freshWorkout.id) {
        if (!this.workout || this.workout.id !== freshWorkout.id) {
          this.workout = freshWorkout
          this.status = 'idle'
        }
      } else {
        this.status = 'idle'
        this.workout = null
      }
    },
  },
  getters: {
    currentExercise: (state) => {
      if (!state.workout || !state.workout.workout_exercises) return null
      return state.workout.workout_exercises[state.currentExerciseIndex]
    },
  },
})
