<template>
  <div>
    <div class="title">
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
      <h1>JYMBRO</h1>
      <font-awesome-icon icon="fa-solid fa-dumbbell" />
    </div>
    <div class="login-container">
      <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
      <form @submit.prevent="handleSubmit" class="login-form">
        <div v-if="!isLogin" class="signup-fields">
          <input v-model="form.username" type="text" placeholder="Username" required />

          <label for="birthdate">Birthdate</label>
          <input id="birthdate" v-model="form.birthdate" type="date" required />

          <label for="gender">Gender</label>
          <select id="gender" v-model="form.gender" required>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <input v-model="form.email" type="email" placeholder="Email" required />
        <input v-model="form.password" type="password" placeholder="Password" required />

        <button type="submit">{{ isLogin ? 'Login' : 'Sign Up' }}</button>
        <p class="switch">
          or <span @click="toggleMode">{{ isLogin ? 'Sign Up' : 'Login' }}</span>
        </p>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  username: '',
  birthdate: '',
  gender: 'male', // Valeur par défaut
})
const error = ref('')
const isLogin = ref(true)

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  form.email = ''
  form.password = ''
  form.username = ''
  form.birthdate = ''
  form.gender = 'male'
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
      birthdate: form.birthdate,
      gender: form.gender,
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
  margin: 30px auto;
  padding: 20px;
  background: #333;
  border-radius: 10px;
  color: #fff;
}

.login-form {
  text-align: center;
}

h2 {
  font-family: Bungee;
  text-align: center;
}

.signup-fields {
  display: flex;
  flex-direction: column;
}
.signup-fields label {
  text-align: left;
  font-size: 12px;
  color: #aaa;
  margin-top: 10px;
  margin-left: 5px;
}

input,
select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #555;
  background: #444;
  color: #fff;
  border-radius: 5px;
  box-sizing: border-box; /* Assure une taille cohérente */
}

button {
  width: 100%;
  background: var(--color-accent);
  color: #fff;
  padding: 15px 30px;
  border: none;
  border-radius: 5px;
  font-family: Quicksand;
  font-weight: 800;
  font-size: 18px;
  margin-top: 20px;
  cursor: pointer;
}

.switch {
  text-align: center;
  font-weight: 400;
  margin-top: 15px;
}
.switch span {
  color: var(--color-accent);
  cursor: pointer;
  text-decoration: underline;
}

.error {
  color: #ff6b6b;
  text-align: center;
}

h1 {
  font-size: 40px;
  font-family: Bungee;
  color: var(--complementary-color);
}

.title {
  font-size: 40px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  gap: 8px;
  margin-top: 30px;
}
</style>
