import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/services/api'
import { useAuthStore } from './auth'

export const useWorkoutStore = defineStore('workout', () => {
  // --- STATE ---
  const workouts = ref([])
  const isLoading = ref(false)
  const currentWorkout = ref(null)

  // --- ACTIONS ---
  async function fetchWorkouts() {
    isLoading.value = true
    workouts.value = []
    const authStore = useAuthStore()

    if (!authStore.user?.id) {
      console.error('User not authenticated or user ID is missing.')
      isLoading.value = false
      return
    }

    try {
      const response = await api.fetchWorkouts(authStore.user.id)
      workouts.value = response.data.workouts
    } catch (error) {
      console.error('Error fetching workouts:', error)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchWorkout(id) {
    isLoading.value = true
    currentWorkout.value = null
    try {
      const response = await api.fetchWorkout(id)
      currentWorkout.value = response.data
    } catch (error) {
      console.error(`Error fetching workout ${id}:`, error)
    } finally {
      isLoading.value = false
    }
  }

  async function createWorkout(workoutData) {
    const authStore = useAuthStore()
    if (!authStore.user?.id) {
      return { success: false, message: 'User not authenticated.' }
    }

    try {
      const workoutPayload = {
        name: workoutData.name,
        user_id: authStore.user.id,
        day_of_week: workoutData.day_of_week,
      }
      const workoutResponse = await api.createWorkout(workoutPayload)
      const newWorkout = workoutResponse.data

      if (workoutData.exercises.length > 0) {
        const exercisesPayload = {
          exercises: workoutData.exercises.map((ex) => ({
            exercise_id: ex.exercise.id,
            planned_sets: ex.planned_sets,
            planned_reps: ex.planned_reps,
            planned_weight: ex.planned_weight,
            rest_seconds: ex.rest_seconds,
            notes: ex.notes,
          })),
        }
        await api.addExercisesToWorkout(newWorkout.id, exercisesPayload)
      }

      return { success: true, newWorkoutId: newWorkout.id }
    } catch (error) {
      console.error('Error creating workout:', error)
      return { success: false, message: error.response?.data?.detail || 'Failed to save workout.' }
    }
  }

  async function updateWorkout(payload) {
    const { id, name, exercises, day_of_week } = payload
    try {
      const updatePayload = {
        name: name,
        day_of_week: day_of_week,
        exercises: exercises.map((ex) => ({
          exercise_id: ex.exercise.id,
          planned_sets: ex.planned_sets,
          planned_reps: ex.planned_reps,
          planned_weight: ex.planned_weight,
          rest_seconds: ex.rest_seconds,
          notes: ex.notes,
        })),
      }

      await api.updateWorkout(id, updatePayload)

      return { success: true }
    } catch (error) {
      console.error('Error updating workout:', error.response?.data)
      return { success: false, message: error.response?.data?.detail?.[0]?.msg || 'Update failed' }
    }
  }

  async function deleteWorkout(id) {
    try {
      await api.deleteWorkout(id)
      return { success: true }
    } catch (error) {
      console.error('Error deleting workout:', error)
      return { success: false, message: 'Delete failed' }
    }
  }

  return {
    workouts,
    isLoading,
    currentWorkout,
    fetchWorkouts,
    fetchWorkout,
    createWorkout,
    updateWorkout,
    deleteWorkout,
  }
})
