<script setup>
import { onBeforeUnmount, watch } from 'vue'
const props = defineProps({
  show: Boolean,
  title: { type: String, default: '' },
  size: { type: String, default: 'lg' },
  closeOnBackdrop: { type: Boolean, default: true },
})
const emit = defineEmits(['close'])
watch(
  () => props.show,
  (show) => {
    document.body.classList.toggle('modal-open', show)
  },
  { immediate: true },
)
onBeforeUnmount(() => document.body.classList.remove('modal-open'))
</script>
<template>
  <Teleport to="body">
    <div
      v-if="show"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      aria-modal="true"
      @mousedown.self="closeOnBackdrop && emit('close')"
    >
      <div
        class="modal-dialog modal-dialog-centered modal-dialog-scrollable"
        :class="`modal-${size}`"
      >
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Cerrar"
              @click="emit('close')"
            ></button>
          </div>
          <div class="modal-body"><slot /></div>
          <div v-if="$slots.footer" class="modal-footer"><slot name="footer" /></div>
        </div>
      </div>
    </div>
    <div v-if="show" class="modal-backdrop fade show"></div>
  </Teleport>
</template>
<style scoped>
.modal-content {
  border: 0;
  border-radius: 1rem;
  box-shadow: 0 24px 70px rgba(18, 28, 45, 0.24);
}
.modal-header,
.modal-footer {
  padding: 1.1rem 1.4rem;
  border-color: #edf0f4;
}
.modal-body {
  padding: 1.4rem;
}
</style>
