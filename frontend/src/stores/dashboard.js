import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/services/api'
import { useAuthStore } from './auth'

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboardData = ref(null)
  const isLoading = ref(false)

  async function fetchData() {
    isLoading.value = true
    const authStore = useAuthStore()
    try {
      const response = await api.fetchDashboardData(authStore.user.id)
      dashboardData.value = response.data
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      isLoading.value = false
    }
  }

  return { dashboardData, isLoading, fetchData }
})
