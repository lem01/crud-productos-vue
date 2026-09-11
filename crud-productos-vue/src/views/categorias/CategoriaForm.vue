<script setup>
import { reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageTabs from '@/components/common/LanguageTabs.vue'
  import { IDIOMAS } from '@/services/categoriaService'
const props = defineProps({ categoria: { type: Object, default: null }, saving: Boolean })
const emit = defineEmits(['submit'])
const { t } = useI18n()
const activeLanguage = ref('es')
const errors = reactive({ codigo: '', nombreEs: '' })
const form = reactive({
  codigo: '',
  activo: true,
  traducciones: { es: { nombre: '', descripcion: '' }, en: { nombre: '', descripcion: '' } },
})

function resetForm(value) {
  form.codigo = value?.codigo || ''
  form.activo = value?.activo ?? true
  form.traducciones.es = {
    nombre: value?.traducciones?.es?.nombre || '',
    descripcion: value?.traducciones?.es?.descripcion || '',
  }
  form.traducciones.en = {
    nombre: value?.traducciones?.en?.nombre || '',
    descripcion: value?.traducciones?.en?.descripcion || '',
  }
  errors.codigo = ''
  errors.nombreEs = ''
  activeLanguage.value = 'es'
}
watch(() => props.categoria, resetForm, { immediate: true })

function submit() {
  errors.codigo = form.codigo.trim() ? '' : t('categories.validation.codeRequired')
  errors.nombreEs = form.traducciones.es.nombre.trim()
    ? ''
    : t('categories.validation.spanishNameRequired')
  if (errors.codigo || errors.nombreEs) {
    if (errors.nombreEs) activeLanguage.value = 'es'
    return
  }
  emit('submit', {
    codigo: form.codigo.trim().toUpperCase(),
    activo: form.activo,
    traducciones: [
      {
        idiomaId: IDIOMAS.es.id,
        nombre: form.traducciones.es.nombre.trim(),
        descripcion: form.traducciones.es.descripcion.trim(),
      },
      {
        idiomaId: IDIOMAS.en.id,
        nombre: form.traducciones.en.nombre.trim(),
        descripcion: form.traducciones.en.descripcion.trim(),
      },
    ],
  })
}
</script>
<template>
  <form id="categoria-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('categories.form.general') }}</h6>
      <div class="row g-3">
        <div class="col-md-7">
          <label class="form-label">{{ t('common.code') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.codigo"
            class="form-control text-uppercase"
            :class="{ 'is-invalid': errors.codigo }"
            maxlength="12"
            :placeholder="t('categories.form.codePlaceholder')"
            @input="errors.codigo = ''"
          />
          <div class="invalid-feedback">{{ errors.codigo }}</div>
          <div class="form-text">{{ t('categories.codeHelp') }}</div>
        </div>
        <div class="col-md-5">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="categoria-activa"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
            /><label class="form-check-label" for="categoria-activa">{{
              form.activo ? t('categories.activeLabel') : t('categories.inactiveLabel')
            }}</label>
          </div>
        </div>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <div class="mb-3">
        <h6 class="section-title mb-1">{{ t('categories.form.translations') }}</h6>
        <p class="text-secondary small mb-0">{{ t('categories.form.translationsHelp') }}</p>
      </div>
      <LanguageTabs v-model="activeLanguage" />
      <div v-show="activeLanguage === 'es'" class="pt-4">
        <div class="mb-3">
          <label class="form-label">{{ t('common.name') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.traducciones.es.nombre"
            class="form-control"
            :class="{ 'is-invalid': errors.nombreEs }"
            :placeholder="t('categories.namePlaceholder')"
            @input="errors.nombreEs = ''"
          />
          <div class="invalid-feedback">{{ errors.nombreEs }}</div>
        </div>
        <div>
          <label class="form-label"
            >{{ t('categories.form.description') }}
            <span class="text-secondary fw-normal"
              >({{ t('categories.form.optional') }})</span
            ></label
          ><textarea
            v-model="form.traducciones.es.descripcion"
            class="form-control"
            rows="3"
            :placeholder="t('categories.form.descriptionPlaceholderEs')"
          ></textarea>
        </div>
      </div>
      <div v-show="activeLanguage === 'en'" class="pt-4">
        <div class="mb-3">
          <label class="form-label"
            >{{ t('categories.form.nameEn') }}
            <span class="text-secondary fw-normal"
              >({{ t('categories.form.optional') }})</span
            ></label
          ><input
            v-model="form.traducciones.en.nombre"
            class="form-control"
            :placeholder="t('categories.form.namePlaceholderEn')"
          />
        </div>
        <div>
          <label class="form-label"
            >{{ t('categories.form.descriptionEn') }}
            <span class="text-secondary fw-normal"
              >({{ t('categories.form.optional') }})</span
            ></label
          ><textarea
            v-model="form.traducciones.en.descripcion"
            class="form-control"
            rows="3"
            :placeholder="t('categories.form.descriptionPlaceholderEn')"
          ></textarea>
        </div>
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
textarea.form-control {
  resize: vertical;
}
</style>
