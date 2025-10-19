import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.token

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

export const api = {
  // --- Authentification ---
  login(email, password) {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    return apiClient.post('/api/users/login', params)
  },
  register(userData) {
    return apiClient.post('/api/users/', userData)
  },
  getCurrentUser() {
    return apiClient.get('/api/users/me')
  },

  // --- Workouts ---
  fetchWorkouts(userId) {
    return apiClient.get('/api/workouts/', { params: { user_id: userId } })
  },
  fetchWorkout(id) {
    return apiClient.get(`/api/workouts/${id}`)
  },
  createWorkout(workoutPayload) {
    return apiClient.post('/api/workouts/', workoutPayload)
  },
  updateWorkout(id, updatePayload) {
    return apiClient.put(`/api/workouts/${id}`, updatePayload)
  },
  deleteWorkout(id) {
    return apiClient.delete(`/api/workouts/${id}`)
  },
  addExercisesToWorkout(workoutId, exercisesPayload) {
    return apiClient.post(`/api/workouts/${workoutId}/exercises`, exercisesPayload)
  },

  // --- Exercises ---
  searchExercises(query) {
    return apiClient.get(`/api/exercises/search/${query}`)
  },

  // --- Logs ---
  createLog(userId, logData) {
    return apiClient.post('/api/logs/', logData, { params: { user_id: userId } })
  },
}
