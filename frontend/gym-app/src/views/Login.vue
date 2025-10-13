<template>
  <div class="login-container">
    <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
    <form @submit.prevent="handleSubmit">
      <input v-if="!isLogin" v-model="form.username" type="text" placeholder="Username" required />
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <button type="submit">{{ isLogin ? 'Login' : 'Sign Up' }}</button>
      <p class="switch">
        or <span @click="toggleMode">{{ isLogin ? 'Sign Up' : 'Login' }}</span>
      </p>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ email: '', password: '', username: '' })
const error = ref('')
const isLogin = ref(true)

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  form.email = ''
  form.password = ''
  form.username = ''
}

const handleSubmit = async () => {
  error.value = ''
  let result

  if (isLogin.value) {
    result = await authStore.login({ email: form.email, password: form.password })
  } else {
    const userData = {
      username: form.username,
      email: form.email,
      password: form.password,
    }
    result = await authStore.register(userData)
  }

  if (result.success) {
    router.push('/home')
  } else {
    error.value = result.message
  }
}
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 50px auto;
  margin-top: 50px;
  padding: 20px;
  background: #333;
  border-radius: 10px;
  color: #fff;
}
h2 {
  text-align: center;
}
input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #555;
  background: #444;
  color: #fff;
  border-radius: 5px;
}
button {
  width: 100%;
  padding: 10px;
  background: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 5px;
  margin: 10px 0;
}
.switch {
  text-align: center;
}
.switch span {
  color: #4a90e2;
  cursor: pointer;
  text-decoration: underline;
}
.error {
  color: #ff6b6b;
  text-align: center;
}
</style>
