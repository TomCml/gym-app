<template>
  <div class="profile-container">
    <h1 class="page-title">Mon Profil</h1>

    <!-- Section d'affichage des informations -->
    <div v-if="!isEditing" class="profile-view">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">
            <span class="avatar-letter">{{ user.username?.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="user-info">
            <h2>{{ user.username }}</h2>
            <p class="email">{{ user.email }}</p>
          </div>
          <button @click="startEditing" class="btn-edit"><span>✏️</span> Modifier</button>
        </div>

        <div class="info-section">
          <h3>Informations personnelles</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Genre</span>
              <span class="value">{{ formatGender(user.gender) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Date de naissance</span>
              <span class="value">{{ formatDate(user.birthdate) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Âge</span>
              <span class="value">{{ calculateAge(user.birthdate) }} ans</span>
            </div>
            <div class="info-item">
              <span class="label">Taille</span>
              <span class="value">{{
                user.height_cm ? user.height_cm + ' cm' : 'Non renseigné'
              }}</span>
            </div>
            <div class="info-item">
              <span class="label">Poids</span>
              <span class="value">{{
                user.weight_kg ? user.weight_kg + ' kg' : 'Non renseigné'
              }}</span>
            </div>
            <div class="info-item">
              <span class="label">Taux de masse grasse</span>
              <span class="value">{{
                user.body_fat_percentage ? user.body_fat_percentage + ' %' : 'Non renseigné'
              }}</span>
            </div>
            <div class="info-item">
              <span class="label">Niveau d'activité</span>
              <span class="value">{{ formatActivityLevel(user.activity_level) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Objectif</span>
              <span class="value">{{ formatGoal(user.goal) }}</span>
            </div>
          </div>
        </div>

        <div class="info-section">
          <h3>Informations du compte</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Membre depuis</span>
              <span class="value">{{ formatDate(user.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Dernière mise à jour</span>
              <span class="value">{{ formatDate(user.updated_at) }}</span>
            </div>
          </div>
        </div>

        <div class="actions-section">
          <button @click="showPasswordModal = true" class="btn-password">
            🔒 Changer le mot de passe
          </button>
        </div>
      </div>
    </div>

    <!-- Section d'édition des informations -->
    <div v-else class="profile-edit">
      <div class="profile-card">
        <h3>Modifier mes informations</h3>
        <form @submit.prevent="saveProfile" class="edit-form">
          <div class="form-group">
            <label for="username">Nom d'utilisateur *</label>
            <input id="username" v-model="editForm.username" type="text" required />
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input id="email" v-model="editForm.email" type="email" required />
          </div>

          <div class="form-group">
            <label for="gender">Genre *</label>
            <select id="gender" v-model="editForm.gender" required>
              <option value="male">Homme</option>
              <option value="female">Femme</option>
            </select>
          </div>

          <div class="form-group">
            <label for="birthdate">Date de naissance *</label>
            <input id="birthdate" v-model="editForm.birthdate" type="date" required />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="height">Taille (cm)</label>
              <input
                id="height"
                v-model.number="editForm.height_cm"
                type="number"
                min="0"
                step="1"
              />
            </div>

            <div class="form-group">
              <label for="weight">Poids (kg)</label>
              <input
                id="weight"
                v-model.number="editForm.weight_kg"
                type="number"
                min="0"
                step="0.1"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="body-fat">Taux de masse grasse (%)</label>
            <input
              id="body-fat"
              v-model.number="editForm.body_fat_percentage"
              type="number"
              min="0"
              max="100"
              step="0.1"
            />
          </div>

          <div class="form-group">
            <label for="activity-level">Niveau d'activité</label>
            <select id="activity-level" v-model="editForm.activity_level">
              <option value="">Non renseigné</option>
              <option value="sedentary">Sédentaire</option>
              <option value="light">Léger</option>
              <option value="moderate">Modéré</option>
              <option value="active">Actif</option>
              <option value="athlete">Athlète</option>
            </select>
          </div>

          <div class="form-group">
            <label for="goal">Objectif</label>
            <select id="goal" v-model="editForm.goal">
              <option value="">Non renseigné</option>
              <option value="lose_weight">Perdre du poids</option>
              <option value="gain_muscle">Gagner du muscle</option>
              <option value="maintain">Maintenir</option>
              <option value="improve_fitness">Améliorer la condition physique</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="button" @click="cancelEdit" class="btn-cancel">Annuler</button>
            <button type="submit" class="btn-save" :disabled="isSaving">
              {{ isSaving ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
          </div>

          <p v-if="updateError" class="error-message">{{ updateError }}</p>
          <p v-if="updateSuccess" class="success-message">Profil mis à jour avec succès !</p>
        </form>
      </div>
    </div>

    <!-- Modal de changement de mot de passe -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Changer le mot de passe</h3>
          <button @click="closePasswordModal" class="btn-close">&times;</button>
        </div>
        <form @submit.prevent="changePassword" class="password-form">
          <div class="form-group">
            <label for="current-password">Mot de passe actuel *</label>
            <input
              id="current-password"
              v-model="passwordForm.currentPassword"
              type="password"
              required
              minlength="8"
            />
          </div>

          <div class="form-group">
            <label for="new-password">Nouveau mot de passe *</label>
            <input
              id="new-password"
              v-model="passwordForm.newPassword"
              type="password"
              required
              minlength="8"
            />
            <small>Minimum 8 caractères</small>
          </div>

          <div class="form-group">
            <label for="confirm-password">Confirmer le nouveau mot de passe *</label>
            <input
              id="confirm-password"
              v-model="passwordForm.confirmPassword"
              type="password"
              required
              minlength="8"
            />
          </div>

          <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
          <p v-if="passwordSuccess" class="success-message">Mot de passe changé avec succès !</p>

          <div class="form-actions">
            <button type="button" @click="closePasswordModal" class="btn-cancel">Annuler</button>
            <button type="submit" class="btn-save" :disabled="isChangingPassword">
              {{ isChangingPassword ? 'Changement...' : 'Changer le mot de passe' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'

const user = ref({})
const isEditing = ref(false)
const isSaving = ref(false)
const updateError = ref('')
const updateSuccess = ref(false)

const editForm = ref({
  username: '',
  email: '',
  gender: '',
  birthdate: '',
  height_cm: null,
  weight_kg: null,
  body_fat_percentage: null,
  activity_level: '',
  goal: '',
})

const showPasswordModal = ref(false)
const isChangingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

onMounted(async () => {
  try {
    const response = await api.getCurrentUser()
    user.value = response.data
  } catch (err) {
    console.error('Error fetching profile', err)
  }
})

const formatGender = (gender) => {
  if (!gender) return 'Non renseigné'
  return gender === 'male' ? 'Homme' : 'Femme'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Non renseigné'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const calculateAge = (birthdate) => {
  if (!birthdate) return 'N/A'
  const today = new Date()
  const birth = new Date(birthdate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  return age
}

const formatActivityLevel = (level) => {
  if (!level) return 'Non renseigné'
  const levels = {
    sedentary: 'Sédentaire',
    light: 'Léger',
    moderate: 'Modéré',
    active: 'Actif',
    athlete: 'Athlète',
  }
  return levels[level] || level
}

const formatGoal = (goal) => {
  if (!goal) return 'Non renseigné'
  const goals = {
    lose_weight: 'Perdre du poids',
    gain_muscle: 'Gagner du muscle',
    maintain: 'Maintenir',
    improve_fitness: 'Améliorer la condition physique',
  }
  return goals[goal] || goal
}

const startEditing = () => {
  // Préparer le formulaire avec les données actuelles
  const birthdate = user.value.birthdate
    ? new Date(user.value.birthdate).toISOString().split('T')[0]
    : ''

  editForm.value = {
    username: user.value.username || '',
    email: user.value.email || '',
    gender: user.value.gender || '',
    birthdate: birthdate,
    height_cm: user.value.height_cm || null,
    weight_kg: user.value.weight_kg || null,
    body_fat_percentage: user.value.body_fat_percentage || null,
    activity_level: user.value.activity_level || '',
    goal: user.value.goal || '',
  }
  isEditing.value = true
  updateError.value = ''
  updateSuccess.value = false
}

const cancelEdit = () => {
  isEditing.value = false
  updateError.value = ''
  updateSuccess.value = false
}

const saveProfile = async () => {
  isSaving.value = true
  updateError.value = ''
  updateSuccess.value = false

  try {
    // Convertir la date au format ISO avec heure
    const birthdateWithTime = new Date(editForm.value.birthdate + 'T00:00:00').toISOString()

    const updateData = {
      username: editForm.value.username,
      email: editForm.value.email,
      gender: editForm.value.gender,
      birthdate: birthdateWithTime,
      height_cm: editForm.value.height_cm || null,
      weight_kg: editForm.value.weight_kg || null,
      body_fat_percentage: editForm.value.body_fat_percentage || null,
      activity_level: editForm.value.activity_level || null,
      goal: editForm.value.goal || null,
    }

    const response = await api.updateCurrentUser(updateData)
    user.value = response.data
    updateSuccess.value = true

    setTimeout(() => {
      isEditing.value = false
      updateSuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Error updating profile', err)
    updateError.value = err.response?.data?.detail || 'Erreur lors de la mise à jour du profil'
  } finally {
    isSaving.value = false
  }
}

const closePasswordModal = () => {
  showPasswordModal.value = false
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
  passwordError.value = ''
  passwordSuccess.value = false
}

const changePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = false

  // Validation
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = 'Les mots de passe ne correspondent pas'
    return
  }

  if (passwordForm.value.newPassword.length < 8) {
    passwordError.value = 'Le nouveau mot de passe doit contenir au moins 8 caractères'
    return
  }

  if (passwordForm.value.currentPassword === passwordForm.value.newPassword) {
    passwordError.value = "Le nouveau mot de passe doit être différent de l'ancien"
    return
  }

  isChangingPassword.value = true

  try {
    await api.changePassword(passwordForm.value.currentPassword, passwordForm.value.newPassword)
    passwordSuccess.value = true

    setTimeout(() => {
      closePasswordModal()
    }, 2000)
  } catch (err) {
    console.error('Error changing password', err)
    passwordError.value = err.response?.data?.detail || 'Erreur lors du changement de mot de passe'
  } finally {
    isChangingPassword.value = false
  }
}
</script>

<style scoped>
h1 {
  margin-top: 10px;
}
h2 {
  font-family: Bungee;
  font-weight: 300;
  font-size: 28px;
  color: var(--complementary-color);
}

h3 {
  margin-top: 0px;
  font-family: Bungee;
  font-weight: 300;
  font-size: 20px;
  color: var(--complementary-color);
}

.profile-container {
  padding: 20px;
  color: var(--complementary-color);
  background-color: var(--color-background);
  max-width: 800px;
  margin: auto;
}

.page-title {
  font-family: Bungee;
  font-weight: 300;
  font-size: 28px;
  margin-bottom: 20px;
  color: var(--complementary-color);
}

.profile-card {
  background: #333;
  border-radius: 8px;
  padding: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #444;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-info h2 {
  margin: 0 0 5px 0;
  font-size: 20px;
  color: var(--complementary-color);
}

.email {
  color: #bbb;
  margin: 0;
  font-size: 14px;
}

.btn-edit {
  padding: 10px 18px;
  background: var(--color-accent);
  border: none;
  color: white;
  border-radius: 60px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-family: Quicksand;
  font-weight: 600;
  transition: ease-in-out 0.1s;
  white-space: nowrap;
}

.btn-edit:hover {
  background: #357abd;
  transform: translateY(-2px);
  scale: 1.05;
}

.info-section {
  margin-bottom: 20px;
}

.info-section h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: var(--complementary-color);
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label {
  font-size: 12px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 16px;
  color: #fff;
  font-weight: 500;
}

.actions-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #444;
}

.btn-password {
  padding: 15px 30px;
  background: var(--color-accent);
  border: none;
  color: white;
  border-radius: 30px;
  cursor: pointer;
  font-family: Quicksand;
  font-weight: 800;
  font-size: 16px;
  transition: ease-in-out 0.1s;
  width: 100%;
}

.btn-password:hover {
  transform: translateY(-2px);
  scale: 1.05;
}

/* Formulaire d'édition */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.form-group label {
  font-size: 14px;
  color: #bbb;
  font-weight: 600;
}

#height,
#weight {
  width: 38vw;
}

.form-group input,
.form-group select {
  padding: 12px;
  background: #222;
  border: 1px solid #444;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-family: Quicksand;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--color-accent);
  background: #2a2a2a;
}

.form-group small {
  font-size: 12px;
  color: #888;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-cancel,
.btn-save {
  padding: 15px 30px;
  border-radius: 30px;
  font-size: 16px;
  cursor: pointer;
  transition: ease-in-out 0.1s;
  border: none;
  font-family: Quicksand;
  font-weight: 800;
  flex: 1;
}

.btn-cancel {
  background: #444;
  color: white;
}

.btn-cancel:hover {
  background: #555;
  transform: translateY(-2px);
  scale: 1.05;
}

.btn-save {
  background: var(--color-accent);
  color: white;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  scale: 1.05;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #333;
  border-radius: 8px;
  padding: 20px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: var(--complementary-color);
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.btn-close:hover {
  background: #444;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Messages */
.error-message {
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.15);
  padding: 12px;
  border-radius: 8px;
  margin: 0;
  font-size: 14px;
}

.success-message {
  color: #51cf66;
  background: rgba(81, 207, 102, 0.15);
  padding: 12px;
  border-radius: 8px;
  margin: 0;
  font-size: 14px;
}

/* Responsive */
@media (min-width: 768px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .profile-header {
    flex-direction: row;
  }

  .btn-password {
    width: auto;
  }
}
</style>
