<template>
  <nav class="bottom-nav">
    <router-link to="/home" class="nav-item">
      <div class="icon">
        <font-awesome-icon icon="fa-regular fa-house" />
      </div>
      <div>Home</div>
    </router-link>

    <router-link to="/workouts" class="nav-item">
      <div class="icon">
        <font-awesome-icon icon="fa-solid fa-dumbbell" />
      </div>
      <div>Workouts</div>
    </router-link>

    <router-link to="/" class="nav-item">
      <div class="icon circle">
        <font-awesome-icon icon="fa-solid fa-circle-play" />
        <div>Start</div>
      </div>
    </router-link>

    <router-link to="/history" class="nav-item">
      <div class="icon">
        <font-awesome-icon icon="fa-solid fa-list" />
      </div>
      <div>History</div>
    </router-link>

    <router-link to="/profile" class="nav-item">
      <div class="icon">
        <font-awesome-icon icon="fa-regular fa-user" />
      </div>
      <div>Profile</div>
    </router-link>
  </nav>
</template>

<script setup></script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background-color: var(--color-background);
  padding: 10px 0;
  border-top: 1px solid #333;
  z-index: 1000;
}

.circle {
  border: solid 3px;
  border-radius: 50px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #888;
  text-decoration: none;
  font-size: 12px;
  width: 50px;
}

.nav-item .icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.router-link-exact-active {
  color: var(--color-accent);
}
</style>
