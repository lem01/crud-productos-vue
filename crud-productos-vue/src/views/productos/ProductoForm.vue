<script setup>
import { reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageTabs from '@/components/common/LanguageTabs.vue'
import { IDIOMAS } from '@/services/productoService'

const props = defineProps({
  producto: { type: Object, default: null },
  categorias: { type: Array, default: () => [] },
  marcas: { type: Array, default: () => [] },
  existingCodes: { type: Array, default: () => [] },
  existingSkus: { type: Array, default: () => [] },
  existingBarcodes: { type: Array, default: () => [] },
  saving: Boolean,
})
const emit = defineEmits(['submit'])
const { t } = useI18n()
const activeLanguage = ref('es')
const errors = reactive({ codigo: '', sku: '', codigoBarras: '', categoriaId: '', nombreEs: '' })
const form = reactive({
  codigo: '',
  sku: '',
  codigoBarras: '',
  categoriaId: '',
  marcaId: '',
  activo: true,
  traducciones: { es: { nombre: '', descripcion: '' }, en: { nombre: '', descripcion: '' } },
})

function resetForm(value) {
  form.codigo = value?.codigo || ''
  form.sku = value?.sku || ''
  form.codigoBarras = value?.codigoBarras || ''
  form.categoriaId = value?.categoriaId ?? ''
  form.marcaId = value?.marcaId ?? ''
  form.activo = value?.activo ?? true
  form.traducciones.es = {
    nombre: value?.traducciones?.es?.nombre || '',
    descripcion: value?.traducciones?.es?.descripcion || '',
  }
  form.traducciones.en = {
    nombre: value?.traducciones?.en?.nombre || '',
    descripcion: value?.traducciones?.en?.descripcion || '',
  }
  for (const key in errors) errors[key] = ''
  activeLanguage.value = 'es'
}

watch(() => props.producto, resetForm, { immediate: true })

function submit() {
  const codigo = form.codigo.trim().toUpperCase()
  const sku = form.sku.trim().toUpperCase()
  const codigoBarras = form.codigoBarras.trim()

  if (!codigo) errors.codigo = t('products.validation.codeRequired')
  else if (props.existingCodes.includes(codigo)) errors.codigo = t('products.validation.codeExists')
  else errors.codigo = ''
  if (!sku) errors.sku = t('products.validation.skuRequired')
  else if (props.existingSkus.includes(sku)) errors.sku = t('products.validation.skuExists')
  else errors.sku = ''
  if (codigoBarras && props.existingBarcodes.includes(codigoBarras))
    errors.codigoBarras = t('products.validation.barcodeExists')
  else errors.codigoBarras = ''
  errors.categoriaId = form.categoriaId === '' ? t('products.validation.categoryRequired') : ''
  errors.nombreEs = form.traducciones.es.nombre.trim()
    ? ''
    : t('products.validation.spanishNameRequired')

  let hasErrors = false
  for (const key in errors) {
    if (errors[key]) hasErrors = true
  }
  if (hasErrors) {
    if (errors.nombreEs) activeLanguage.value = 'es'
    return
  }

  const traducciones = []
  traducciones.push({
    idiomaId: IDIOMAS.es.id,
    nombre: form.traducciones.es.nombre.trim(),
    descripcion: form.traducciones.es.descripcion.trim(),
  })
  const nombreEn = form.traducciones.en.nombre.trim()
  const descripcionEn = form.traducciones.en.descripcion.trim()
  if (nombreEn || descripcionEn)
    traducciones.push({ idiomaId: IDIOMAS.en.id, nombre: nombreEn, descripcion: descripcionEn })

  emit('submit', {
    codigo,
    sku,
    codigoBarras: codigoBarras || null,
    categoriaId: Number(form.categoriaId),
    marcaId: form.marcaId === '' ? null : Number(form.marcaId),
    activo: form.activo,
    traducciones,
  })
}
</script>

<template>
  <form id="producto-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('common.generalInfo') }}</h6>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">{{ t('common.code') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.codigo"
            class="form-control text-uppercase"
            :class="{ 'is-invalid': errors.codigo }"
            maxlength="30"
            :placeholder="t('products.form.codePlaceholder')"
            :disabled="saving"
            @input="errors.codigo = ''"
          />
          <div class="invalid-feedback">{{ errors.codigo }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label">SKU <span class="text-danger">*</span></label
          ><input
            v-model="form.sku"
            class="form-control text-uppercase"
            :class="{ 'is-invalid': errors.sku }"
            maxlength="40"
            :placeholder="t('products.form.skuPlaceholder')"
            :disabled="saving"
            @input="errors.sku = ''"
          />
          <div class="invalid-feedback">{{ errors.sku }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label">{{ t('products.barcode') }}</label
          ><input
            v-model="form.codigoBarras"
            class="form-control"
            :class="{ 'is-invalid': errors.codigoBarras }"
            maxlength="50"
            :placeholder="t('products.form.barcodePlaceholder')"
            :disabled="saving"
            @input="errors.codigoBarras = ''"
          />
          <div class="invalid-feedback">{{ errors.codigoBarras }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="producto-activo"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
              :disabled="saving"
            /><label class="form-check-label" for="producto-activo">{{
              form.activo ? t('products.activeLabel') : t('products.inactiveLabel')
            }}</label>
          </div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('products.category') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.categoriaId"
            class="form-select"
            :class="{ 'is-invalid': errors.categoriaId }"
            :disabled="saving"
            @change="errors.categoriaId = ''"
          >
            <option value="" disabled>{{ t('products.form.selectCategory') }}</option>
            <option v-for="item in categorias" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.categoriaId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('products.brand') }}
            <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><select v-model="form.marcaId" class="form-select" :disabled="saving">
            <option value="">{{ t('products.noBrand') }}</option>
            <option v-for="item in marcas" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
        </div>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <div class="mb-3">
        <h6 class="section-title mb-1">{{ t('common.translations') }}</h6>
        <p class="text-secondary small mb-0">{{ t('common.translationsHelp') }}</p>
      </div>
      <LanguageTabs v-model="activeLanguage" />
      <div v-show="activeLanguage === 'es'" class="pt-4">
        <div class="mb-3">
          <label class="form-label">{{ t('common.name') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.traducciones.es.nombre"
            class="form-control"
            :class="{ 'is-invalid': errors.nombreEs }"
            :placeholder="t('products.form.namePlaceholderEs')"
            :disabled="saving"
            @input="errors.nombreEs = ''"
          />
          <div class="invalid-feedback">{{ errors.nombreEs }}</div>
        </div>
        <div>
          <label class="form-label"
            >{{ t('common.description') }}
            <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><textarea
            v-model="form.traducciones.es.descripcion"
            class="form-control"
            rows="3"
            :placeholder="t('products.form.descriptionPlaceholderEs')"
            :disabled="saving"
          ></textarea>
        </div>
      </div>
      <div v-show="activeLanguage === 'en'" class="pt-4">
        <div class="mb-3">
          <label class="form-label"
            >Name <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><input
            v-model="form.traducciones.en.nombre"
            class="form-control"
            :placeholder="t('products.form.namePlaceholderEn')"
            :disabled="saving"
          />
        </div>
        <div>
          <label class="form-label"
            >Description
            <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><textarea
            v-model="form.traducciones.en.descripcion"
            class="form-control"
            rows="3"
            :placeholder="t('products.form.descriptionPlaceholderEn')"
            :disabled="saving"
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
