<script setup>
import { useI18n } from 'vue-i18n'
defineProps({ active: { type: Boolean, required: true } })
const { t } = useI18n()
</script>
<template>
  <span class="status-badge" :class="active ? 'active' : 'inactive'"
    ><span class="status-dot"></span>{{ active ? t('common.active') : t('common.inactive') }}</span
  >
</template>
<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.38rem;
  padding: 0.3rem 0.58rem;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 600;
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
.active {
  color: #137454;
  background: #e7f7f1;
}
.inactive {
  color: #7a8495;
  background: #eef0f3;
}
</style>
