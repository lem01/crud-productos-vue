<script setup>
import { reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageTabs from '@/components/common/LanguageTabs.vue'
import { IDIOMAS } from '@/services/marcaService'

const props = defineProps({ marca: { type: Object, default: null }, saving: Boolean })
const emit = defineEmits(['submit'])
const { t } = useI18n()
const activeLanguage = ref('es')
const errors = reactive({ nombreEs: '' })
const form = reactive({
  activo: true,
  traducciones: { es: { nombre: '' }, en: { nombre: '' } },
})

function resetForm(value) {
  form.activo = value?.activo ?? true
  form.traducciones.es.nombre = value?.traducciones?.es?.nombre || ''
  form.traducciones.en.nombre = value?.traducciones?.en?.nombre || ''
  errors.nombreEs = ''
  activeLanguage.value = 'es'
}

watch(() => props.marca, resetForm, { immediate: true })

function submit() {
  const nombreEs = form.traducciones.es.nombre.trim()
  errors.nombreEs = nombreEs ? '' : t('brands.validation.spanishNameRequired')
  if (errors.nombreEs) {
    activeLanguage.value = 'es'
    return
  }

  const nombreEn = form.traducciones.en.nombre.trim()
  const traducciones = [{ idiomaId: IDIOMAS.es.id, nombre: nombreEs }]
  if (nombreEn) traducciones.push({ idiomaId: IDIOMAS.en.id, nombre: nombreEn })
  emit('submit', { activo: form.activo, traducciones })
}
</script>

<template>
  <form id="marca-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('brands.form.general') }}</h6>
      <div class="row g-3">
        <div class="col-md-7">
          <p class="text-secondary small mb-0">{{ t('brands.form.generalHelp') }}</p>
        </div>
        <div class="col-md-5">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="marca-activa"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
              :disabled="saving"
            />
            <label class="form-check-label" for="marca-activa">
              {{ form.activo ? t('brands.activeLabel') : t('brands.inactiveLabel') }}
            </label>
          </div>
        </div>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <div class="mb-3">
        <h6 class="section-title mb-1">{{ t('common.translations') }}</h6>
        <p class="text-secondary small mb-0">{{ t('brands.form.translationsHelp') }}</p>
      </div>
      <LanguageTabs v-model="activeLanguage" />
      <div v-show="activeLanguage === 'es'" class="pt-4">
        <label class="form-label">{{ t('common.name') }} <span class="text-danger">*</span></label>
        <input
          v-model="form.traducciones.es.nombre"
          class="form-control"
          :class="{ 'is-invalid': errors.nombreEs }"
          :placeholder="t('brands.namePlaceholder')"
          :disabled="saving"
          @input="errors.nombreEs = ''"
        />
        <div class="invalid-feedback">{{ errors.nombreEs }}</div>
      </div>
      <div v-show="activeLanguage === 'en'" class="pt-4">
        <label class="form-label">
          {{ t('brands.form.nameEn') }}
          <span class="text-secondary fw-normal">({{ t('common.optional') }})</span>
        </label>
        <input
          v-model="form.traducciones.en.nombre"
          class="form-control"
          :placeholder="t('brands.form.namePlaceholderEn')"
          :disabled="saving"
        />
      </div>
    </section>
  </form>
</template>

<style scoped>
.section-title {
  color: #2a3447;
  font-weight: 700;
}
.form-label {
  font-size: 0.84rem;
  font-weight: 600;
}
.status-switch {
  display: flex;
  align-items: center;
  min-height: 42px;
  gap: 0.55rem;
  padding: 0 0.9rem;
  border: 1px solid #dce1e9;
  border-radius: 0.55rem;
  background: #fafbfc;
}
.status-switch .form-check-input {
  margin: 0;
}
</style>
