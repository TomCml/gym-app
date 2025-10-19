<template>
  <div>
    <Loader :show="isLoading" />

    <div class="stats-container" v-if="!isLoading">
      <div class="header">
        <h2>Statistics</h2>
      </div>

      <div v-if="workouts.length > 0">
        <div class="chart-section">
          <h3>Progress per Exercise</h3>
          <select v-model="selectedExercise" class="exercise-select">
            <option disabled value="">Please select an exercise</option>
            <option v-for="exercise in uniqueExercises" :key="exercise" :value="exercise">
              {{ exercise }}
            </option>
          </select>
          <div v-if="selectedExercise" class="chart-container">
            <Line :data="exerciseProgressChartData" :options="chartOptions" />
          </div>
          <div v-else class="empty-chart">
            <p>Select an exercise to see your progress.</p>
          </div>
        </div>

        <div class="chart-section">
          <h3>Daily Volume</h3>
          <div class="chart-container">
            <Bar :data="volumeChartData" :options="chartOptions" />
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>You don't have any workout logs yet.</p>
        <p>Complete some workouts to see your stats!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useWorkoutStore } from '../stores/workout'
import { Line, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
)

const workoutStore = useWorkoutStore()
const { workouts, isLoading } = storeToRefs(workoutStore)

const selectedExercise = ref('')

onMounted(() => {
  if (workouts.value.length === 0) {
    workoutStore.fetchWorkouts()
  }
})

const uniqueExercises = computed(() => {
  const exercises = new Set()
  workouts.value.forEach((workout) => {
    workout.workout_exercises.forEach((we) => {
      exercises.add(we.exercise.name)
    })
  })
  return Array.from(exercises).sort()
})

const exerciseProgressChartData = computed(() => {
  if (!selectedExercise.value) {
    return { labels: [], datasets: [] }
  }

  const filteredWorkouts = workouts.value
    .filter((w) => w.workout_exercises.some((we) => we.exercise.name === selectedExercise.value))
    .sort((a, b) => new Date(a.date) - new Date(b.date))

  const labels = filteredWorkouts.map((w) => new Date(w.date).toLocaleDateString('fr-FR'))

  const data = filteredWorkouts.map((w) => {
    const workoutExercise = w.workout_exercises.find(
      (we) => we.exercise.name === selectedExercise.value,
    )
    let maxWeight = 0
    if (workoutExercise && workoutExercise.sets) {
      workoutExercise.sets.forEach((set) => {
        if (set.weight > maxWeight) {
          maxWeight = set.weight
        }
      })
    }
    return maxWeight
  })

  return {
    labels,
    datasets: [
      {
        label: `Max Weight for ${selectedExercise.value} (kg)`,
        data,
        borderColor: '#4a90e2',
        backgroundColor: 'rgba(74, 144, 226, 0.5)',
        tension: 0.1,
      },
    ],
  }
})

const volumeChartData = computed(() => {
  const workoutsByDate = {}
  workouts.value.forEach((w) => {
    const date = new Date(w.date).toLocaleDateString('fr-FR')
    if (!workoutsByDate[date]) {
      workoutsByDate[date] = 0
    }
    let dailyVolume = 0
    w.workout_exercises.forEach((we) => {
      if (we.sets) {
        we.sets.forEach((set) => {
          dailyVolume += (set.reps || 0) * (set.weight || 0)
        })
      }
    })
    workoutsByDate[date] += dailyVolume
  })

  const sortedDates = Object.keys(workoutsByDate).sort((a, b) => {
    const dateA = a.split('/').reverse().join('-')
    const dateB = b.split('/').reverse().join('-')
    return new Date(dateA) - new Date(dateB)
  })

  const labels = sortedDates
  const data = sortedDates.map((date) => workoutsByDate[date])

  return {
    labels,
    datasets: [
      {
        label: 'Daily Workout Volume (kg)',
        data,
        backgroundColor: '#4a90e2',
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#fff',
      },
    },
  },
  scales: {
    y: {
      ticks: {
        color: '#bbb',
      },
      grid: {
        color: '#444',
      },
    },
    x: {
      ticks: {
        color: '#bbb',
      },
      grid: {
        color: '#444',
      },
    },
  },
}
</script>

<style scoped>
h2,
h3 {
  font-family: Bungee;
  font-weight: 300;
}

h2 {
  font-size: 28px;
}

h3 {
  font-size: 22px;
  margin-bottom: 15px;
}

.stats-container {
  padding: 20px;
  color: var(--complementary-color);
  background-color: #101922;
  max-width: 800px;
  margin: auto;
}

.header {
  margin-bottom: 20px;
}

.empty-state,
.empty-chart {
  text-align: center;
  margin-top: 40px;
  color: #aaa;
}

.chart-section {
  background-color: #333;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.exercise-select {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  background-color: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-family: Quicksand;
}

.chart-container {
  position: relative;
  height: 40vh;
}
</style>
