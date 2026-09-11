<script setup>
import { ref } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppNavbar from './AppNavbar.vue'
const sidebarOpen = ref(false)
</script>
<template>
  <div class="app-shell">
    <AppSidebar :open="sidebarOpen" @close="sidebarOpen = false" />
    <div class="app-main">
      <AppNavbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="app-content"><RouterView /></main>
    </div>
  </div>
</template>
