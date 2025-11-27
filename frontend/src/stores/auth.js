import { defineStore } from 'pinia'
import { api } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.login(credentials.email, credentials.password)
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        return { success: true }
      } catch (error) {
        console.error('Login failed:', error.response?.data)
        return { success: false, message: error.response?.data?.detail || 'An error occurred' }
      }
    },

    async register(userData) {
      try {
        await api.register(userData)

        return await this.login({ email: userData.email, password: userData.password })
      } catch (error) {
        console.error('Register failed:', error.response?.data)
        return { success: false, message: error.response?.data?.detail || 'Registration failed' }
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})
