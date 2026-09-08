<script setup>
defineProps({ text: { type: String, default: 'Cargando...' } })
</script>
<template>
  <div class="d-flex align-items-center justify-content-center gap-2 py-5 text-secondary">
    <span class="spinner-border spinner-border-sm text-primary" role="status"></span
    ><span>{{ text }}</span>
  </div>
</template>
