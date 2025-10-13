// src/stores/exercise.js

import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const EXERCISES_API_URL = 'http://localhost:8000/api/exercises'

export const useExerciseStore = defineStore('exercise', () => {
  // --- STATE ---
  const searchResults = ref([])
  const isLoading = ref(false)

  // --- ACTIONS ---
  async function searchExercises(query) {
    if (query.length < 2) {
      searchResults.value = []
      return
    }
    isLoading.value = true
    try {
      const response = await axios.get(`${EXERCISES_API_URL}/search/${query}`)
      searchResults.value = response.data
    } catch (error) {
      console.error('Error searching exercises:', error)
      searchResults.value = []
    } finally {
      isLoading.value = false
    }
  }

  function clearSearchResults() {
    searchResults.value = []
  }

  return { searchResults, isLoading, searchExercises, clearSearchResults }
})
