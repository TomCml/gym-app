<template>
  <Transition name="fade">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <h4>{{ title }}</h4>
        <p>{{ message }}</p>
        <div class="modal-actions">
          <button class="btn-secondary" @click="$emit('close')">Non</button>
          <button class="btn-danger" @click="$emit('confirm')">Oui</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Confirmation',
  },
  message: {
    type: String,
    required: true,
  },
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}

.modal-content {
  background-color: #2a2a2a;
  padding: 25px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

h4 {
  margin-top: 0;
  font-size: 18px;
}

p {
  color: #ccc;
  margin-bottom: 25px;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.modal-actions button {
  padding: 10px 30px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.btn-secondary {
  background-color: #555;
  color: #fff;
}

.btn-danger {
  background-color: #e53e3e;
  color: #fff;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
