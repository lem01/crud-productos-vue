<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const props = defineProps({
  modelValue: { type: String, required: true },
  languages: {
    type: Array,
    default: null,
  },
})
defineEmits(['update:modelValue'])
const { t } = useI18n()
const visibleLanguages = computed(
  () =>
    props.languages || [
      { code: 'es', label: t('common.spanish'), note: t('common.mainLanguage'), required: true },
      { code: 'en', label: t('common.english'), note: t('common.languageOptional') },
    ],
)
</script>
<template>
  <ul class="nav language-tabs">
    <li v-for="lang in visibleLanguages" :key="lang.code" class="nav-item">
      <button
        type="button"
        class="nav-link"
        :class="{ active: modelValue === lang.code }"
        @click="$emit('update:modelValue', lang.code)"
      >
        <span>{{ lang.label }} <strong v-if="lang.required" class="text-danger">*</strong></span
        ><small>{{ lang.note }}</small>
      </button>
    </li>
  </ul>
</template>
<style scoped>
.language-tabs {
  gap: 0.35rem;
  padding: 0.3rem;
  border: 1px solid var(--app-border);
  border-radius: 0.7rem;
  background: #f6f7f9;
}
.nav-link {
  min-width: 135px;
  padding: 0.55rem 0.8rem;
  border-radius: 0.5rem;
  color: #687386;
  text-align: left;
}
.nav-link span,
.nav-link small {
  display: block;
}
.nav-link span {
  font-weight: 600;
}
.nav-link small {
  margin-top: 0.1rem;
  font-size: 0.67rem;
}
.nav-link.active {
  color: #284bbd;
  background: white;
  box-shadow: 0 2px 8px rgba(28, 39, 60, 0.08);
}
</style>
