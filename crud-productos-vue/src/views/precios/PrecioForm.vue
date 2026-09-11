<script setup>
import { reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  precioItem: { type: Object, default: null },
  productos: { type: Array, default: () => [] },
  centros: { type: Array, default: () => [] },
  monedas: { type: Array, default: () => [] },
  saving: Boolean,
})
const emit = defineEmits(['submit'])
const { t, locale } = useI18n()
const errors = reactive({
  productoId: '',
  centroDistribucionId: '',
  monedaId: '',
  precio: '',
  fechaInicio: '',
  fechaFin: '',
})
const form = reactive({
  productoId: '',
  centroDistribucionId: '',
  monedaId: '',
  precio: '',
  fechaInicio: '',
  fechaFin: '',
  activo: true,
})

function obtenerFecha(value) {
  if (!value) return ''
  return value.slice(0, 10)
}

function resetForm(value) {
  form.productoId = value?.productoId ?? ''
  form.centroDistribucionId = value?.centroDistribucionId ?? ''
  form.monedaId = value?.monedaId ?? ''
  form.precio = value?.precio ?? ''
  form.fechaInicio = obtenerFecha(value?.fechaInicio)
  form.fechaFin = obtenerFecha(value?.fechaFin)
  form.activo = value?.activo ?? true
  for (const key in errors) errors[key] = ''
}

watch(() => props.precioItem, resetForm, { immediate: true })

function nombreMoneda(moneda) {
  const traduccion = moneda.traducciones[locale.value] || moneda.traducciones.es
  return traduccion.nombre
}

function clearDateErrors() {
  errors.fechaInicio = ''
  errors.fechaFin = ''
}

function submit() {
  const price = Number(form.precio)
  errors.productoId = form.productoId === '' ? t('prices.validation.productRequired') : ''
  errors.centroDistribucionId =
    form.centroDistribucionId === '' ? t('prices.validation.centerRequired') : ''
  errors.monedaId = form.monedaId === '' ? t('prices.validation.currencyRequired') : ''
  errors.precio =
    form.precio === '' || !Number.isFinite(price) || price <= 0
      ? t('prices.validation.positivePrice')
      : ''
  errors.fechaInicio = form.fechaInicio ? '' : t('prices.validation.startDateRequired')
  if (form.fechaFin && form.fechaInicio && form.fechaFin < form.fechaInicio)
    errors.fechaFin = t('prices.validation.invalidEndDate')
  else errors.fechaFin = ''

  let hasErrors = false
  for (const key in errors) {
    if (errors[key]) hasErrors = true
  }
  if (hasErrors) return

  emit('submit', {
    productoId: Number(form.productoId),
    centroDistribucionId: Number(form.centroDistribucionId),
    monedaId: Number(form.monedaId),
    precio: price,
    fechaInicio: `${form.fechaInicio}T00:00:00`,
    fechaFin: form.fechaFin ? `${form.fechaFin}T00:00:00` : null,
    activo: form.activo,
  })
}
</script>

<template>
  <form id="precio-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('prices.form.title') }}</h6>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('prices.product') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.productoId"
            class="form-select"
            :class="{ 'is-invalid': errors.productoId }"
            :disabled="saving"
            @change="errors.productoId = ''"
          >
            <option value="" disabled>{{ t('prices.form.selectProduct') }}</option>
            <option v-for="item in productos" :key="item.id" :value="item.id">
              {{ item.codigo }} — {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.productoId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('prices.center') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.centroDistribucionId"
            class="form-select"
            :class="{ 'is-invalid': errors.centroDistribucionId }"
            :disabled="saving"
            @change="errors.centroDistribucionId = ''"
          >
            <option value="" disabled>{{ t('prices.form.selectCenter') }}</option>
            <option v-for="item in centros" :key="item.id" :value="item.id">
              {{ item.codigo }} — {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.centroDistribucionId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('prices.currency') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.monedaId"
            class="form-select"
            :class="{ 'is-invalid': errors.monedaId }"
            :disabled="saving"
            @change="errors.monedaId = ''"
          >
            <option value="" disabled>{{ t('prices.form.selectCurrency') }}</option>
            <option v-for="item in monedas" :key="item.id" :value="item.id">
              {{ item.codigo }} — {{ nombreMoneda(item) }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.monedaId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('prices.price') }} <span class="text-danger">*</span></label
          ><input
            v-model="form.precio"
            type="number"
            min="0"
            step="0.01"
            class="form-control"
            :class="{ 'is-invalid': errors.precio }"
            placeholder="0.00"
            :disabled="saving"
            @input="errors.precio = ''"
          />
          <div class="invalid-feedback">{{ errors.precio }}</div>
        </div>
        <div class="col-md-6">
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
        <div class="col-md-6">
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
        <div class="col-12">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="precio-activo"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
              :disabled="saving"
            /><label class="form-check-label" for="precio-activo">{{
              form.activo ? t('prices.activeLabel') : t('prices.inactiveLabel')
            }}</label>
          </div>
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
</style>
