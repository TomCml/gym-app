<template>
  <div>
    <div class="page-container">
      <div class="header">
        <button @click="router.back()" class="close-btn">✕</button>
        <h2>Edit Workout</h2>
        <button class="delete-button" @click="isDeleteModalVisible = true">
          <font-awesome-icon icon="fa-solid fa-trash" />
        </button>
      </div>

      <Loader :show="workoutStore.isLoading" />

      <div v-if="!workoutStore.isLoading && currentWorkout" class="form-content">
        <div class="form-group">
          <label for="workoutName">Workout Name</label>
          <input id="workoutName" v-model="workoutName" class="input-field" />
        </div>
        <div class="form-group">
          <label for="dayOfWeek">Day of the Week</label>
          <select id="dayOfWeek" v-model="dayOfWeek" class="input-field">
            <option :value="null">Not planned</option>
            <option :value="1">Monday</option>
            <option :value="2">Tuesday</option>
            <option :value="3">Wednesday</option>
            <option :value="4">Thursday</option>
            <option :value="5">Friday</option>
            <option :value="6">Saturday</option>
            <option :value="7">Sunday</option>
          </select>
        </div>

        <div class="form-group exercise-group">
          <label>Exercises</label>
          <ul class="added-exercises-list">
            <li
              v-for="(exercise, index) in addedExercises"
              :key="exercise.id || index"
              class="exercise-item"
            >
              <div class="exercise-header">
                <span>{{ exercise.exercise ? exercise.exercise.name : exercise.name }}</span>
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

      <div class="footer" v-if="!workoutStore.isLoading && currentWorkout">
        <div class="footer-buttons">
          <button class="save-button" @click="handleUpdate" :disabled="!isFormValid">Update</button>
        </div>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>

    <ConfirmationModal
      :show="isDeleteModalVisible"
      title="Delete Workout"
      message="Are you sure you want to delete this workout?"
      @close="isDeleteModalVisible = false"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<script setup>
// Le script est correct et reste inchangé
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useWorkoutStore } from '../stores/workout'
import { useExerciseStore } from '../stores/exercise'
import { useDebounceFn } from '@vueuse/core'
import ConfirmationModal from '../components/ConfirmationModale.vue'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const workoutStore = useWorkoutStore()
const exerciseStore = useExerciseStore()

const { searchResults } = storeToRefs(exerciseStore)
const { currentWorkout } = storeToRefs(workoutStore)

const workoutName = ref('')
const dayOfWeek = ref(null)
const addedExercises = ref([])
const searchQuery = ref('')
const isSearchActive = ref(false)
const errorMessage = ref('')
const isDeleteModalVisible = ref(false)

onMounted(() => {
  workoutStore.fetchWorkout(props.id)
})

watch(
  currentWorkout,
  (newVal) => {
    if (newVal) {
      workoutName.value = newVal.name
      dayOfWeek.value = newVal.day_of_week
      addedExercises.value = newVal.workout_exercises
    }
  },
  { immediate: true },
)

const isFormValid = computed(
  () => workoutName.value.trim() !== '' && addedExercises.value.length > 0,
)

const debouncedSearch = useDebounceFn(() => {
  exerciseStore.searchExercises(searchQuery.value)
}, 300)

const addExercise = (exercise) => {
  const existingExercise = addedExercises.value.find((e) => e.exercise.id === exercise.id)
  if (!existingExercise) {
    addedExercises.value.push({
      exercise: exercise,
      planned_sets: 3,
      planned_reps: 10,
      planned_weight: 0,
      rest_seconds: 60,
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

const handleUpdate = async () => {
  if (!isFormValid.value) return
  const result = await workoutStore.updateWorkout({
    id: props.id,
    name: workoutName.value,
    day_of_week: dayOfWeek.value,
    exercises: addedExercises.value,
  })
  if (result.success) {
    await workoutStore.fetchWorkouts()
    router.push('/workouts')
  } else {
    errorMessage.value = result.message
  }
}

const handleDeleteConfirm = async () => {
  isDeleteModalVisible.value = false
  const result = await workoutStore.deleteWorkout(props.id)
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
  font-family: 'Quicksand', sans-serif;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--color-background);
  color: #fff;
}

.header,
.footer {
  flex-shrink: 0;
}

.header {
  padding: 15px;
  text-align: center;
  position: relative;
  border-bottom: 1px solid #222;
}

.form-content {
  flex-grow: 1;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 10px;

  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.exercise-group {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 0;
  margin-bottom: 0;
}

.added-exercises-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
  overflow-y: auto;
  width: 100vw;
}

.search-container {
  flex-shrink: 0;
  margin-top: 15px;
  position: relative;
}

.footer {
  padding: 10px;
  border-top: 1px solid #222;
  background-color: var(--color-background);
  text-align: center;
}

.header h2 {
  margin: 0;
  font-size: 24px;
  font-family: Bungee;
  color: var(--complementary-color);
  font-weight: 400;
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
  color: var(--complementary-color);
  font-weight: bold;
}

.input-field,
.detail-input input,
.notes-input input {
  transition: border-color 0.2s ease-in-out;
}

.input-field:focus,
.detail-input input:focus,
.notes-input input:focus {
  outline: none;
  border-color: var(--complementary-color);
}

.input-field {
  width: 100%;
  max-width: 430px;
  padding: 15px;
  background: #1e1e1e;
  border: 1px solid #333;
  color: #fff;
  border-radius: 8px;
  font-size: 16px;
  font-family: 'Quicksand', sans-serif;
}
select.input-field {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url('data:image/svg+xml;charset=UTF8,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%2724%27%20height%3D%2724%27%20viewBox%3D%270%200%2024%2024%27%3E%3Cpath%20fill%3D%27%23aaa%27%20d%3D%27M7%2010l5%205%205-5z%27%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 15px center;
  background-size: 20px;
  font-family: 'Quicksand', sans-serif;
}

.exercise-item {
  background: #2a2a2a;
  padding: 15px;
  margin-bottom: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  width: 90vw;
  height: 20vh;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.exercise-details {
  font-family: 'Quicksand', sans-serif;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.detail-input {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 40px;
}

.detail-input label {
  font-size: 11px;
  color: #aaa;
  margin-bottom: 5px;
}

.detail-input input {
  font-family: 'Quicksand', sans-serif;
  width: 16.5vw;
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
  font-family: 'Quicksand', sans-serif;
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
  bottom: 72%;
  width: 100%;
  max-width: 90vw;
  background: #2a2a2a;
  border: 1px var(--complementary-color) solid;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.result-item,
.loading-item {
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: #333 2px solid;
}

.result-item:hover {
  background: var(--color-accent);
}

.save-button {
  background: var(--color-accent);
  font-family: Quicksand;
  font-weight: 500;
  color: #fff;
  padding: 0;
  border: none;
  width: 20vw;
  height: 4vh;
  border-radius: 30px;
  font-size: 16px;
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

.footer-buttons {
  display: flex;
  gap: 10px;
}

.delete-button {
  background-color: #e53e3e;
  font-family: Quicksand, sans-serif;
  font-weight: 500;
  color: #fff;
  padding: 0;
  border: none;
  width: 15vw;
  height: 4vh;
  border-radius: 30px;
  font-size: 16px;
  cursor: pointer;
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
}

.save-button {
  flex-grow: 1;
}
</style>
