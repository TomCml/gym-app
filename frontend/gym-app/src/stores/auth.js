import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/users'

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
      const params = new URLSearchParams()
      params.append('username', credentials.email)
      params.append('password', credentials.password)

      try {
        const response = await axios.post(`${API_URL}/login`, params)

        this.token = response.data.access_token
        this.user = response.data.user

        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))

        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        return { success: true }
      } catch (error) {
        console.error('Login failed:', error.response?.data)
        return { success: false, message: error.response?.data?.detail || 'An error occurred' }
      }
    },

    async register(userData) {
      try {
        await axios.post(API_URL + '/', userData)

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
      delete axios.defaults.headers.common['Authorization']
    },
  },
})
