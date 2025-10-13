// src/stores/workout.js

import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

const WORKOUTS_API_URL = 'http://localhost:8000/api/workouts'

export const useWorkoutStore = defineStore('workout', () => {
  // --- STATE (variables) ---
  const workouts = ref([])
  const isLoading = ref(false)

  // --- ACTION 1 ---
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
      const response = await axios.get(WORKOUTS_API_URL, {
        params: { user_id: authStore.user.id },
      })
      workouts.value = response.data.workouts
    } catch (error) {
      console.error('Error fetching workouts:', error)
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
      }
      const workoutResponse = await axios.post(WORKOUTS_API_URL, workoutPayload)
      const newWorkout = workoutResponse.data

      if (workoutData.exercises.length > 0) {
        const exercisesPayload = {
          exercises: workoutData.exercises.map((ex) => ({
            exercise_id: ex.id,
            planned_sets: ex.planned_sets,
            planned_reps: ex.planned_reps,
            planned_weight: ex.planned_weight,
            rest_seconds: ex.rest_seconds, // ✨ CHAMP AJOUTÉ
            notes: ex.notes, // ✨ CHAMP AJOUTÉ
          })),
        }
        await axios.post(`${WORKOUTS_API_URL}/${newWorkout.id}/exercises`, exercisesPayload)
      }

      return { success: true, newWorkoutId: newWorkout.id }
    } catch (error) {
      console.error('Error creating workout:', error)
      return { success: false, message: error.response?.data?.detail || 'Failed to save workout.' }
    }
  }

  return {
    workouts,
    isLoading,
    fetchWorkouts,
    createWorkout,
  }
})
