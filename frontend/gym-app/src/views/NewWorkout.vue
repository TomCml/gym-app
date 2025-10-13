<template>
  <div class="page-container">
    <div class="header">
      <button @click="router.back()" class="close-btn">✕</button>
      <h2>New Workout</h2>
    </div>

    <div class="form-content">
      <div class="form-group">
        <label for="workoutName">Workout Name</label>
        <input
          id="workoutName"
          v-model="workoutName"
          placeholder="e.g. Morning Pump"
          class="input-field"
        />
      </div>

      <div class="form-group exercise-group">
        <label>Exercises</label>

        <ul class="added-exercises-list">
          <li v-for="(exercise, index) in addedExercises" :key="exercise.id" class="exercise-item">
            <div class="exercise-header">
              <span>{{ exercise.name }}</span>
              <button @click="removeExercise(index)" class="remove-btn">−</button>
            </div>
            <div class="exercise-details">
              <div class="detail-input">
                <label>Sets</label>
                <input type="number" v-model.number="exercise.planned_sets" />
              </div>
              <div class="detail-input">
                <label>Reps</label>
                <input type="number" v-model.number="exercise.planned_reps" />
              </div>
              <div class="detail-input">
                <label>Weight (kg)</label>
                <input type="number" step="0.5" v-model.number="exercise.planned_weight" />
              </div>
              <div class="detail-input">
                <label>Rest (s)</label>
                <input type="number" step="5" v-model.number="exercise.rest_seconds" />
              </div>
            </div>
            <div class="notes-input">
              <input type="text" v-model="exercise.notes" placeholder="Add notes..." />
            </div>
          </li>
        </ul>

        <div class="search-container">
          <input
            v-model="searchQuery"
            placeholder="Add Exercise"
            class="input-field search-input"
            @input="debouncedSearch"
            @focus="isSearchActive = true"
          />
          <span class="search-icon">⊕</span>
          <ul
            v-if="isSearchActive && (exerciseStore.isLoading || searchResults.length)"
            class="search-results"
          >
            <li v-if="exerciseStore.isLoading" class="loading-item">Searching...</li>
            <li
              v-for="result in searchResults"
              :key="result.id"
              @click="addExercise(result)"
              class="result-item"
            >
              {{ result.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer">
      <button class="save-button" @click="saveWorkout" :disabled="!isFormValid">
        Save Workout
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useWorkoutStore } from '../stores/workout'
import { useExerciseStore } from '../stores/exercise'
import { useDebounceFn } from '@vueuse/core'

const router = useRouter()
const workoutStore = useWorkoutStore()
const exerciseStore = useExerciseStore()
const { searchResults } = storeToRefs(exerciseStore)
const workoutName = ref('')
const addedExercises = ref([])
const searchQuery = ref('')
const isSearchActive = ref(false)
const errorMessage = ref('')

const isFormValid = computed(
  () => workoutName.value.trim() !== '' && addedExercises.value.length > 0,
)

const debouncedSearch = useDebounceFn(() => {
  exerciseStore.searchExercises(searchQuery.value)
}, 300)

const addExercise = (exercise) => {
  if (!addedExercises.value.some((e) => e.id === exercise.id)) {
    addedExercises.value.push({
      ...exercise,
      planned_sets: 3,
      planned_reps: 10,
      planned_weight: 0,
      rest_seconds: 90,
      notes: '',
    })
  }
  searchQuery.value = ''
  exerciseStore.clearSearchResults()
  isSearchActive.value = false
}

const removeExercise = (index) => {
  addedExercises.value.splice(index, 1)
}

const saveWorkout = async () => {
  if (!isFormValid.value) return

  const result = await workoutStore.createWorkout({
    name: workoutName.value,
    exercises: addedExercises.value,
  })

  if (result.success) {
    await workoutStore.fetchWorkouts()
    router.push('/workouts')
  } else {
    errorMessage.value = result.message
  }
}
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: calc(
    100vh - 80px
  ); /* Hauteur de l'écran moins la barre de nav du bas (ajustez si besoin) */
  background-color: var(--color-background);
  color: #fff;
}

.header,
.footer {
  flex-shrink: 0; /* Empêche ces éléments de rétrécir */
}

.header {
  padding: 15px;
  text-align: center;
  position: relative;
  border-bottom: 1px solid #222;
}

.form-content {
  flex-grow: 1; /* Prend tout l'espace vertical restant */
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Empêche le contenu de déborder de manière non contrôlée */
}

.exercise-group {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 0; /* Astuce flexbox pour que l'overflow fonctionne correctement */
  margin-bottom: 0;
}

.added-exercises-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1; /* Fait scroller la liste */
  overflow-y: auto; /* Affiche une barre de scroll si nécessaire */
  padding-right: 5px;
}

.search-container {
  flex-shrink: 0; /* La barre de recherche ne rétrécit pas */
  margin-top: 15px;
  position: relative;
}

.footer {
  padding: 20px;
  border-top: 1px solid #222;
  background-color: var(--color-background);
}

.header h2 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #aaa;
  font-weight: bold;
}

.input-field {
  width: 100%;
  padding: 15px;
  background: #1e1e1e;
  border: 1px solid #333;
  color: #fff;
  border-radius: 8px;
  font-size: 16px;
}

.exercise-item {
  background: #2a2a2a;
  padding: 15px;
  margin-bottom: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.exercise-details {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.detail-input {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 60px; /* Assure que les inputs ne deviennent pas trop petits */
}

.detail-input label {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 5px;
}

.detail-input input {
  width: 100%;
  padding: 8px;
  background: #1e1e1e;
  border: 1px solid #444;
  color: #fff;
  border-radius: 5px;
  text-align: center;
  font-size: 16px;
}

.notes-input {
  margin-top: 10px;
  width: 100%;
}
.notes-input input {
  width: 100%;
  padding: 8px;
  background: #1e1e1e;
  border: 1px solid #444;
  color: #fff;
  border-radius: 5px;
  font-size: 14px;
}

.remove-btn {
  background: #444;
  border: none;
  color: #fff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
}

.search-input {
  padding-right: 40px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-accent);
  font-size: 24px;
}

.search-results {
  list-style: none;
  padding: 0;
  margin-top: 5px;
  position: absolute;
  bottom: 100%;
  width: 100%;
  background: #2a2a2a;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.result-item,
.loading-item {
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #333;
}

.result-item:hover {
  background: var(--color-accent);
}

.save-button {
  background: var(--color-accent);
  color: #fff;
  padding: 15px;
  border: none;
  width: 100%;
  border-radius: 30px;
  font-size: 18px;
  cursor: pointer;
}

.save-button:disabled {
  background: #333;
  cursor: not-allowed;
}

.error-message {
  color: #ff6b6b;
  text-align: center;
  margin-top: 10px;
}
</style>
