<!-- src/views/History.vue (logs graphs, simple list + chart) -->
<template>
  <div class="history">
    <h2>History</h2>
    <ul>
      <li v-for="log in logs" :key="log.id">
        {{ log.exercise.name }} - Sets: {{ log.set_number }}, Reps: {{ log.reps }}, Weight:
        {{ log.weight }}
      </li>
    </ul>
    <div class="chart">
      <LineChart v-if="chartData.labels.length" :data="chartData" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Line as LineChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale)

const logs = ref([])
const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Reps over time',
      data: [],
      borderColor: '#4a90e2',
    },
  ],
})

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/users/1/logs')
    logs.value = response.data
    // Simple chart data
    chartData.value.labels = logs.value.map((l) => l.date)
    chartData.value.datasets[0].data = logs.value.map((l) => l.reps)
  } catch (err) {
    console.error('Error fetching logs', err)
  }
})
</script>

<style scoped>
h2 {
  font-family: Bungee;
  font-weight: 300;
}
.history {
  padding: 20px;
  color: #fff;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  background: #333;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}
.chart {
  margin-top: 20px;
}
</style>
