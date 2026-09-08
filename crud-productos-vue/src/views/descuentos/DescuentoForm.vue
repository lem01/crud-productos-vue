<script setup>
import { reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageTabs from '@/components/common/LanguageTabs.vue'
import { IDIOMAS } from '@/services/descuentoService'

const props = defineProps({
  descuento: { type: Object, default: null },
  centros: { type: Array, default: () => [] },
  tipos: { type: Array, default: () => [] },
  productos: { type: Array, default: () => [] },
  saving: Boolean,
})
const emit = defineEmits(['submit'])
const { t } = useI18n()
const activeLanguage = ref('es')
const errors = reactive({
  codigo: '',
  centroDistribucionId: '',
  valor: '',
  fechaInicio: '',
  fechaFin: '',
  nombreEs: '',
})
const form = reactive({
  codigo: '',
  centroDistribucionId: '',
  tipoDescuentoId: '',
  valor: '',
  fechaInicio: '',
  fechaFin: '',
  activo: true,
  productos: [],
  traducciones: { es: { nombre: '', descripcion: '' }, en: { nombre: '', descripcion: '' } },
})

function obtenerFecha(value) {
  if (!value) return ''
  return value.slice(0, 10)
}

function resetForm(value) {
  form.codigo = value?.codigo || ''
  form.centroDistribucionId = value?.centroDistribucionId ?? ''
  form.tipoDescuentoId = props.tipos.find((item) => item.codigo === 'PORCENTAJE')?.id ?? ''
  form.valor = value?.valor ?? ''
  form.fechaInicio = obtenerFecha(value?.fechaInicio)
  form.fechaFin = obtenerFecha(value?.fechaFin)
  form.activo = value?.activo ?? true
  form.productos = []
  if (value?.productos)
    value.productos.forEach((item) =>
      form.productos.push({
        productoId: item.productoId,
        prioridad: item.prioridad ?? 0,
        activo: item.activo ?? true,
      }),
    )
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

watch(() => props.descuento, resetForm, { immediate: true })
watch(
  () => props.tipos,
  (tipos) => {
    form.tipoDescuentoId = tipos.find((item) => item.codigo === 'PORCENTAJE')?.id ?? ''
  },
  { immediate: true },
)

function isProductSelected(id) {
  return form.productos.some((item) => item.productoId === id)
}

function productSelectionChanged(producto, event) {
  if (event.target.checked)
    form.productos.push({ productoId: producto.id, prioridad: 0, activo: true })
  else {
    const index = form.productos.findIndex((item) => item.productoId === producto.id)
    if (index >= 0) form.productos.splice(index, 1)
  }
}

function selectedProduct(id) {
  return form.productos.find((item) => item.productoId === id)
}

function clearDateErrors() {
  errors.fechaInicio = ''
  errors.fechaFin = ''
}

function submit() {
  const value = Number(form.valor)
  errors.codigo = form.codigo.trim() ? '' : t('discounts.validation.codeRequired')
  errors.centroDistribucionId =
    form.centroDistribucionId === '' ? t('discounts.validation.centerRequired') : ''
  if (form.valor === '' || !Number.isFinite(value) || value <= 0)
    errors.valor = t('discounts.validation.positiveValue')
  else if (value > 100) errors.valor = t('discounts.validation.percentageMaximum')
  else errors.valor = ''
  errors.fechaInicio = form.fechaInicio ? '' : t('discounts.validation.startDateRequired')
  errors.fechaFin =
    form.fechaFin && form.fechaInicio && form.fechaFin < form.fechaInicio
      ? t('discounts.validation.invalidEndDate')
      : ''
  errors.nombreEs = form.traducciones.es.nombre.trim()
    ? ''
    : t('discounts.validation.spanishNameRequired')

  let hasErrors = false
  for (const key in errors) if (errors[key]) hasErrors = true
  if (hasErrors) {
    if (errors.nombreEs) activeLanguage.value = 'es'
    return
  }

  const traducciones = [
    {
      idiomaId: IDIOMAS.es.id,
      nombre: form.traducciones.es.nombre.trim(),
      descripcion: form.traducciones.es.descripcion.trim(),
    },
  ]
  const nombreEn = form.traducciones.en.nombre.trim()
  const descripcionEn = form.traducciones.en.descripcion.trim()
  if (nombreEn || descripcionEn)
    traducciones.push({ idiomaId: IDIOMAS.en.id, nombre: nombreEn, descripcion: descripcionEn })
  const productos = []
  form.productos.forEach((item) =>
    productos.push({
      productoId: Number(item.productoId),
      prioridad: Number(item.prioridad || 0),
      activo: item.activo,
    }),
  )

  emit('submit', {
    codigo: form.codigo.trim().toUpperCase(),
    centroDistribucionId: Number(form.centroDistribucionId),
    tipoDescuentoId: Number(form.tipoDescuentoId),
    valor: value,
    monedaId: null,
    fechaInicio: `${form.fechaInicio}T00:00:00`,
    fechaFin: form.fechaFin ? `${form.fechaFin}T23:59:59` : null,
    activo: form.activo,
    traducciones,
    productos,
  })
}
</script>

<template>
  <form id="descuento-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('common.generalInfo') }}</h6>
      <div class="row g-3">
        <div class="col-md-4">
          <label class="form-label">{{ t('common.code') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.codigo"
            class="form-control text-uppercase"
            :class="{ 'is-invalid': errors.codigo }"
            maxlength="30"
            :disabled="saving"
            @input="errors.codigo = ''"
          />
          <div class="invalid-feedback">{{ errors.codigo }}</div>
        </div>
        <div class="col-md-4">
          <label class="form-label"
            >{{ t('discounts.center') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.centroDistribucionId"
            class="form-select"
            :class="{ 'is-invalid': errors.centroDistribucionId }"
            :disabled="saving"
            @change="errors.centroDistribucionId = ''"
          >
            <option value="" disabled>{{ t('discounts.form.selectCenter') }}</option>
            <option v-for="item in centros" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.centroDistribucionId }}</div>
        </div>
        <div class="col-md-4">
          <label class="form-label"
            >{{ t('discounts.value') }} <span class="text-danger">*</span></label
          >
          <div class="input-group has-validation">
            <input
              v-model="form.valor"
              type="number"
              min="0"
              step="0.01"
              class="form-control"
              :class="{ 'is-invalid': errors.valor }"
              :disabled="saving"
              @input="errors.valor = ''"
            /><span class="input-group-text">%</span>
            <div class="invalid-feedback">{{ errors.valor }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <label class="form-label"
            >{{ t('common.startDate') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.fechaInicio"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': errors.fechaInicio }"
            :disabled="saving"
            @input="clearDateErrors"
          />
          <div class="invalid-feedback">{{ errors.fechaInicio }}</div>
        </div>
        <div class="col-md-4">
          <label class="form-label"
            >{{ t('common.endDate') }}
            <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><input
            v-model="form.fechaFin"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': errors.fechaFin }"
            :disabled="saving"
            @input="errors.fechaFin = ''"
          />
          <div class="invalid-feedback">{{ errors.fechaFin }}</div>
        </div>
        <div class="col-md-4">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="descuento-activo"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
              :disabled="saving"
            /><label class="form-check-label" for="descuento-activo">{{
              form.activo ? t('discounts.activeLabel') : t('discounts.inactiveLabel')
            }}</label>
          </div>
        </div>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <h6 class="section-title">{{ t('discounts.applicableProducts') }}</h6>
      <p class="text-secondary small">{{ t('discounts.form.productsHelp') }}</p>
      <div class="product-list border rounded p-2">
        <div v-for="item in productos" :key="item.id" class="product-row py-1">
          <div class="form-check">
            <input
              :id="`discount-product-${item.id}`"
              class="form-check-input"
              type="checkbox"
              :checked="isProductSelected(item.id)"
              :disabled="saving"
              @change="productSelectionChanged(item, $event)"
            /><label class="form-check-label" :for="`discount-product-${item.id}`"
              ><strong>{{ item.codigo }}</strong> — {{ item.nombre }}</label
            >
          </div>
          <div v-if="isProductSelected(item.id)" class="priority-field">
            <label class="small text-secondary">{{ t('discounts.priority') }}</label
            ><input
              v-model="selectedProduct(item.id).prioridad"
              type="number"
              min="0"
              step="1"
              class="form-control form-control-sm"
              :disabled="saving"
            />
          </div>
        </div>
        <p v-if="!productos.length" class="text-secondary small mb-0">
          {{ t('discounts.form.noProducts') }}
        </p>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <div class="mb-3">
        <h6 class="section-title mb-1">{{ t('common.translations') }}</h6>
        <p class="text-secondary small mb-0">{{ t('discounts.form.translationsHelp') }}</p>
      </div>
      <LanguageTabs v-model="activeLanguage" />
      <div v-show="activeLanguage === 'es'" class="pt-4">
        <div class="mb-3">
          <label class="form-label">{{ t('common.name') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.traducciones.es.nombre"
            class="form-control"
            :class="{ 'is-invalid': errors.nombreEs }"
            :disabled="saving"
            @input="errors.nombreEs = ''"
          />
          <div class="invalid-feedback">{{ errors.nombreEs }}</div>
        </div>
        <label class="form-label">{{ t('common.description') }}</label
        ><textarea
          v-model="form.traducciones.es.descripcion"
          class="form-control"
          rows="3"
          :disabled="saving"
        ></textarea>
      </div>
      <div v-show="activeLanguage === 'en'" class="pt-4">
        <div class="mb-3">
          <label class="form-label"
            >Name <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
          ><input v-model="form.traducciones.en.nombre" class="form-control" :disabled="saving" />
        </div>
        <label class="form-label"
          >Description
          <span class="text-secondary fw-normal">({{ t('common.optional') }})</span></label
        ><textarea
          v-model="form.traducciones.en.descripcion"
          class="form-control"
          rows="3"
          :disabled="saving"
        ></textarea>
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
.product-list {
  max-height: 240px;
  overflow-y: auto;
  background: #fafbfc;
}
.product-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.priority-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.priority-field input {
  width: 80px;
}
textarea.form-control {
  resize: vertical;
}
</style>
