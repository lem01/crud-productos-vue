<script setup>
import BaseModal from './BaseModal.vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const props = defineProps({
  show: Boolean,
  title: { type: String, default: '' },
  message: { type: String, required: true },
  confirmText: { type: String, default: '' },
  confirmClass: { type: String, default: 'btn-danger' },
  loading: Boolean,
})
defineEmits(['close', 'confirm'])
const { t } = useI18n()
const modalTitle = computed(() => props.title || t('common.confirmAction'))
const buttonText = computed(() => props.confirmText || t('common.confirm'))
</script>
<template>
  <BaseModal
    :show="show"
    :title="modalTitle"
    size="sm"
    :close-on-backdrop="!loading"
    @close="$emit('close')"
    ><div class="text-center px-2 py-2">
      <span class="confirm-icon"><i class="bi bi-exclamation-triangle"></i></span>
      <p class="mb-0 mt-3 text-secondary">{{ message }}</p>
    </div>
    <template #footer
      ><button class="btn btn-light" :disabled="loading" @click="$emit('close')">
        {{ t('common.cancel') }}</button
      ><button class="btn" :class="confirmClass" :disabled="loading" @click="$emit('confirm')">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>{{ buttonText }}
      </button></template
    ></BaseModal
  >
</template>
<style scoped>
.confirm-icon {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  margin: auto;
  border-radius: 50%;
  color: #c2413b;
  background: #fff0ef;
  font-size: 1.45rem;
}
</style>
