<script setup>
import { reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  inventario: { type: Object, default: null },
  productos: { type: Array, default: () => [] },
  centros: { type: Array, default: () => [] },
  existingCombinations: { type: Array, default: () => [] },
  saving: Boolean,
})
const emit = defineEmits(['submit'])
const { t } = useI18n()
const errors = reactive({
  productoId: '',
  centroDistribucionId: '',
  cantidadDisponible: '',
  cantidadReservada: '',
  cantidadMinima: '',
  cantidadMaxima: '',
  combination: '',
})
const form = reactive({
  productoId: '',
  centroDistribucionId: '',
  cantidadDisponible: 0,
  cantidadReservada: 0,
  cantidadMinima: '',
  cantidadMaxima: '',
})

function resetForm(value) {
  form.productoId = value?.productoId ?? ''
  form.centroDistribucionId = value?.centroDistribucionId ?? ''
  form.cantidadDisponible = value?.cantidadDisponible ?? 0
  form.cantidadReservada = value?.cantidadReservada ?? 0
  form.cantidadMinima = value?.cantidadMinima ?? ''
  form.cantidadMaxima = value?.cantidadMaxima ?? ''
  for (const key in errors) errors[key] = ''
}

watch(() => props.inventario, resetForm, { immediate: true })

function validateQuantity(field) {
  const value = form[field]
  if (value !== '' && (!Number.isFinite(Number(value)) || Number(value) < 0))
    errors[field] = t('inventory.validation.nonNegative')
  else errors[field] = ''
}

function clearSelectionErrors() {
  errors.productoId = ''
  errors.centroDistribucionId = ''
  errors.combination = ''
}

function submit() {
  errors.productoId = form.productoId === '' ? t('inventory.validation.productRequired') : ''
  errors.centroDistribucionId =
    form.centroDistribucionId === '' ? t('inventory.validation.centerRequired') : ''
  validateQuantity('cantidadDisponible')
  validateQuantity('cantidadReservada')
  validateQuantity('cantidadMinima')
  validateQuantity('cantidadMaxima')

  if (!errors.productoId && !errors.centroDistribucionId) {
    const key = `${Number(form.productoId)}-${Number(form.centroDistribucionId)}`
    errors.combination = props.existingCombinations.includes(key)
      ? t('inventory.validation.combinationExists')
      : ''
  }

  const disponible = form.cantidadDisponible === '' ? 0 : Number(form.cantidadDisponible)
  const reservada = form.cantidadReservada === '' ? 0 : Number(form.cantidadReservada)
  if (!errors.cantidadDisponible && !errors.cantidadReservada && reservada > disponible)
    errors.cantidadReservada = t('inventory.validation.reservedExceedsAvailable')

  if (
    !errors.cantidadMinima &&
    !errors.cantidadMaxima &&
    form.cantidadMinima !== '' &&
    form.cantidadMaxima !== '' &&
    Number(form.cantidadMinima) > Number(form.cantidadMaxima)
  )
    errors.cantidadMaxima = t('inventory.validation.minimumExceedsMaximum')

  let hasErrors = false
  for (const key in errors) {
    if (errors[key]) hasErrors = true
  }
  if (hasErrors) return

  emit('submit', {
    productoId: Number(form.productoId),
    centroDistribucionId: Number(form.centroDistribucionId),
    cantidadDisponible: disponible,
    cantidadReservada: reservada,
    cantidadMinima: form.cantidadMinima === '' ? null : Number(form.cantidadMinima),
    cantidadMaxima: form.cantidadMaxima === '' ? null : Number(form.cantidadMaxima),
  })
}
</script>

<template>
  <form id="inventario-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('inventory.form.location') }}</h6>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('inventory.product') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.productoId"
            class="form-select"
            :class="{ 'is-invalid': errors.productoId || errors.combination }"
            :disabled="saving"
            @change="clearSelectionErrors"
          >
            <option value="" disabled>{{ t('inventory.form.selectProduct') }}</option>
            <option v-for="item in productos" :key="item.id" :value="item.id">
              {{ item.codigo }} — {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.productoId || errors.combination }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('inventory.center') }} <span class="text-danger">*</span></label
          ><select
            v-model="form.centroDistribucionId"
            class="form-select"
            :class="{ 'is-invalid': errors.centroDistribucionId || errors.combination }"
            :disabled="saving"
            @change="clearSelectionErrors"
          >
            <option value="" disabled>{{ t('inventory.form.selectCenter') }}</option>
            <option v-for="item in centros" :key="item.id" :value="item.id">
              {{ item.codigo }} — {{ item.nombre }}
            </option>
          </select>
          <div class="invalid-feedback">
            {{ errors.centroDistribucionId || errors.combination }}
          </div>
        </div>
      </div>
    </section>
    <hr class="my-4" />
    <section>
      <h6 class="section-title">{{ t('inventory.form.quantities') }}</h6>
      <div class="row g-3">
        <div
          v-for="field in [
            { key: 'cantidadDisponible', label: t('inventory.available') },
            { key: 'cantidadReservada', label: t('inventory.reserved') },
            { key: 'cantidadMinima', label: t('inventory.minimum') },
            { key: 'cantidadMaxima', label: t('inventory.maximum') },
          ]"
          :key="field.key"
          class="col-md-6"
        >
          <label class="form-label">{{ field.label }}</label
          ><input
            v-model="form[field.key]"
            type="number"
            min="0"
            step="1"
            class="form-control"
            :class="{ 'is-invalid': errors[field.key] }"
            :disabled="saving"
            @input="errors[field.key] = ''"
          />
          <div class="invalid-feedback">{{ errors[field.key] }}</div>
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
</style>
