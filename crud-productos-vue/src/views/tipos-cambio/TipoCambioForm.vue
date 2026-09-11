<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  tipoCambio: { type: Object, default: null },
  monedas: { type: Array, default: () => [] },
  saving: Boolean,
})
const emit = defineEmits(['submit'])
const { t, locale } = useI18n()
const errors = reactive({
  monedaOrigenId: '',
  monedaDestinoId: '',
  tasa: '',
  fechaInicio: '',
  fechaFin: '',
})
const form = reactive({
  monedaOrigenId: '',
  monedaDestinoId: '',
  tasa: '',
  fechaInicio: '',
  fechaFin: '',
  activo: true,
})
const lastRelation = ref('')

function obtenerFecha(value) {
  if (!value) return ''
  return value.slice(0, 10)
}

function resetForm(value) {
  form.monedaOrigenId = value?.monedaOrigenId ?? ''
  form.monedaDestinoId = value?.monedaDestinoId ?? ''
  form.tasa = value?.tasa ?? ''
  form.fechaInicio = obtenerFecha(value?.fechaInicio)
  form.fechaFin = obtenerFecha(value?.fechaFin)
  form.activo = value?.activo ?? true
  lastRelation.value = `${form.monedaOrigenId}-${form.monedaDestinoId}`
  for (const key in errors) errors[key] = ''
}

watch(() => props.tipoCambio, resetForm, { immediate: true })

function nombreMoneda(moneda) {
  const traduccion = moneda.traducciones[locale.value] || moneda.traducciones.es
  return traduccion.nombre
}

function currencyById(id) {
  return props.monedas.find((moneda) => moneda.id === Number(id))
}

const conversionExample = computed(() => {
  const origen = currencyById(form.monedaOrigenId)
  const destino = currencyById(form.monedaDestinoId)
  const tasa = Number(form.tasa)
  if (!origen || !destino || !Number.isFinite(tasa) || tasa <= 0) return ''
  const resultado = 100 * tasa
  const valor = new Intl.NumberFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    maximumFractionDigits: 8,
  }).format(resultado)
  return t('exchangeRates.form.example', {
    origin: origen.codigo,
    destination: destino.codigo,
    result: valor,
  })
})

function handleCurrencyChange() {
  errors.monedaOrigenId = ''
  errors.monedaDestinoId = ''
  const currentRelation = `${form.monedaOrigenId}-${form.monedaDestinoId}`
  if (lastRelation.value && currentRelation !== lastRelation.value) form.tasa = ''
  lastRelation.value = currentRelation
}

function clearDateErrors() {
  errors.fechaInicio = ''
  errors.fechaFin = ''
}

function submit() {
  const origenId = Number(form.monedaOrigenId)
  const destinoId = Number(form.monedaDestinoId)
  const tasa = Number(form.tasa)

  errors.monedaOrigenId =
    form.monedaOrigenId === '' ? t('exchangeRates.validation.originRequired') : ''
  if (form.monedaDestinoId === '')
    errors.monedaDestinoId = t('exchangeRates.validation.destinationRequired')
  else if (origenId === destinoId)
    errors.monedaDestinoId = t('exchangeRates.validation.differentCurrencies')
  else errors.monedaDestinoId = ''
  errors.tasa =
    form.tasa === '' || !Number.isFinite(tasa) || tasa <= 0
      ? t('exchangeRates.validation.positiveRate')
      : ''
  errors.fechaInicio = form.fechaInicio ? '' : t('exchangeRates.validation.startDateRequired')
  if (form.fechaFin && form.fechaInicio && form.fechaFin < form.fechaInicio)
    errors.fechaFin = t('exchangeRates.validation.invalidEndDate')
  else errors.fechaFin = ''

  let hasErrors = false
  for (const key in errors) {
    if (errors[key]) hasErrors = true
  }
  if (hasErrors) return

  emit('submit', {
    monedaOrigenId: origenId,
    monedaDestinoId: destinoId,
    tasa,
    fechaInicio: `${form.fechaInicio}T00:00:00`,
    fechaFin: form.fechaFin ? `${form.fechaFin}T00:00:00` : null,
    activo: form.activo,
  })
}
</script>

<template>
  <form id="tipo-cambio-form" novalidate @submit.prevent="submit">
    <section>
      <h6 class="section-title">{{ t('exchangeRates.form.title') }}</h6>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('exchangeRates.originCurrency') }} <span class="text-danger">*</span></label
          >
          <select
            v-model="form.monedaOrigenId"
            class="form-select"
            :class="{ 'is-invalid': errors.monedaOrigenId }"
            :disabled="saving"
            @change="handleCurrencyChange"
          >
            <option value="" disabled>{{ t('exchangeRates.form.selectCurrency') }}</option>
            <option v-for="moneda in monedas" :key="moneda.id" :value="moneda.id">
              {{ moneda.codigo }} — {{ nombreMoneda(moneda) }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.monedaOrigenId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('exchangeRates.destinationCurrency') }} <span class="text-danger">*</span></label
          >
          <select
            v-model="form.monedaDestinoId"
            class="form-select"
            :class="{ 'is-invalid': errors.monedaDestinoId }"
            :disabled="saving"
            @change="handleCurrencyChange"
          >
            <option value="" disabled>{{ t('exchangeRates.form.selectCurrency') }}</option>
            <option v-for="moneda in monedas" :key="moneda.id" :value="moneda.id">
              {{ moneda.codigo }} — {{ nombreMoneda(moneda) }}
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.monedaDestinoId }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('exchangeRates.rate') }} <span class="text-danger">*</span></label
          >
          <input
            v-model="form.tasa"
            type="number"
            min="0"
            step="0.00000001"
            class="form-control"
            :class="{ 'is-invalid': errors.tasa }"
            placeholder="0.00000000"
            :disabled="saving"
            @input="errors.tasa = ''"
          />
          <div class="invalid-feedback">{{ errors.tasa }}</div>
        </div>
        <div class="col-md-6">
          <label class="form-label d-block">{{ t('common.status') }}</label>
          <div class="form-check form-switch status-switch">
            <input
              id="tipo-cambio-activo"
              v-model="form.activo"
              class="form-check-input"
              type="checkbox"
              :disabled="saving"
            /><label class="form-check-label" for="tipo-cambio-activo">{{
              form.activo ? t('exchangeRates.activeLabel') : t('exchangeRates.inactiveLabel')
            }}</label>
          </div>
        </div>
        <div class="col-md-6">
          <label class="form-label"
            >{{ t('common.startDate') }} <span class="text-danger">*</span></label
          >
          <input
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
          >
          <input
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
          <div class="conversion-help">
            <strong>{{ t('exchangeRates.form.formula') }}</strong>
            <span v-if="conversionExample" class="d-block mt-1">{{ conversionExample }}</span>
            <span v-else class="d-block mt-1 text-secondary">{{
              t('exchangeRates.form.exampleHelp')
            }}</span>
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
.conversion-help {
  padding: 0.75rem 0.9rem;
  border: 1px solid #dce1e9;
  border-radius: 0.55rem;
  color: #42506a;
  background: #f8f9fb;
  font-size: 0.84rem;
}
</style>
