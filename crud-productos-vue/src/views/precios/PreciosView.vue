<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { MONEDAS } from '@/constants/monedas'
import {
  actualizarPrecio,
  cambiarEstadoPrecio,
  crearPrecio,
  listarCentrosPrecio,
  listarPrecios,
  listarProductosPrecio,
  obtenerPrecio,
} from '@/services/precioService'
import { manejarErrorApi, obtenerMensajeRespuesta } from '@/utils/apiResponse'
import PrecioForm from './PrecioForm.vue'

const { t, locale } = useI18n()
const precios = ref([])
const productos = ref([])
const centros = ref([])
const monedas = ref(MONEDAS)
const cargando = ref(false)
const guardando = ref(false)
const search = ref('')
const center = ref('all')
const status = ref('all')
const formOpen = ref(false)
const editing = ref(null)
const confirmOpen = ref(false)
const selected = ref(null)
const notice = ref('')
const serviceError = ref('')

const filtered = computed(() => {
  return precios.value.filter((item) => {
    const term = search.value.trim().toLowerCase()
    const codigo = (item.productoCodigo || '').toLowerCase()
    const nombre = (item.productoNombre || '').toLowerCase()
    const matchesText = !term || codigo.includes(term) || nombre.includes(term)
    const matchesCenter =
      center.value === 'all' || item.centroDistribucionId === Number(center.value)
    const matchesStatus = status.value === 'all' || item.activo === (status.value === 'active')
    return matchesText && matchesCenter && matchesStatus
  })
})

const groupedByCenter = computed(() => {
  const groups = new Map()

  filtered.value.forEach((item) => {
    const key = item.centroDistribucionId ?? item.centroDistribucionNombre
    if (!groups.has(key)) {
      groups.set(key, {
        id: key,
        nombre: item.centroDistribucionNombre,
        codigo: item.centroDistribucionCodigo,
        items: [],
      })
    }
    groups.get(key).items.push(item)
  })

  return [...groups.values()]
})

onMounted(load)
watch(locale, load)

function getErrorMessage(error) {
  if (error.message) return error.message
  return t('prices.loadError')
}

async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    const respuestas = await Promise.all([
      listarPrecios(locale.value),
      listarProductosPrecio(locale.value),
      listarCentrosPrecio(locale.value),
    ])
    precios.value = respuestas[0]
    productos.value = respuestas[1]
    centros.value = respuestas[2]
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    cargando.value = false
  }
}

function create() {
  editing.value = null
  serviceError.value = ''
  formOpen.value = true
}

async function edit(item) {
  guardando.value = true
  serviceError.value = ''
  try {
    editing.value = await obtenerPrecio(item.id, locale.value)
    formOpen.value = true
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function showNotice(message) {
  notice.value = message
  setTimeout(() => {
    notice.value = ''
  }, 3000)
}

async function save(data) {
  if (guardando.value) return
  guardando.value = true
  serviceError.value = ''
  try {
    const response = editing.value
      ? await actualizarPrecio(editing.value.id, data, locale.value)
      : await crearPrecio(data, locale.value)
    const mensaje = obtenerMensajeRespuesta(response)

    await load()
    formOpen.value = false
    if (mensaje) showNotice(mensaje)
  } catch (error) {
    serviceError.value = manejarErrorApi(error)
  } finally {
    guardando.value = false
  }
}

function askStatus(item) {
  selected.value = item
  confirmOpen.value = true
}

async function toggleStatus() {
  if (guardando.value) return
  guardando.value = true
  serviceError.value = ''
  try {
    const response = await cambiarEstadoPrecio(selected.value.id)
    const mensaje = obtenerMensajeRespuesta(response)

    await load()
    confirmOpen.value = false
    if (mensaje) showNotice(mensaje)
  } catch (error) {
    serviceError.value = manejarErrorApi(error)
  } finally {
    guardando.value = false
  }
}

function formatCurrency(value, currencyCode) {
  if (value == null || value === '' || !Number.isFinite(Number(value))) return '—'

  return new Intl.NumberFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    style: 'currency',
    currency: currencyCode,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value))
}

function hasDiscount(item) {
  return Boolean(item.descuentoNombre || Number(item.montoDescuento) > 0)
}

function discountType(item) {
  if (item.tipoDescuento === 'PORCENTAJE') return t('prices.percentage')
  if (item.tipoDescuento === 'MONTO_FIJO') return t('prices.fixedAmount')
  return item.tipoDescuento || t('prices.notAvailable')
}

function discountValue(item) {
  if (item.valorDescuento == null) return '—'
  if (item.tipoDescuento === 'PORCENTAJE') return `${Number(item.valorDescuento)}%`
  return formatCurrency(item.valorDescuento, item.monedaCodigo || 'HNL')
}

function formatExchangeRate(value) {
  if (value == null || !Number.isFinite(Number(value))) return '—'
  return new Intl.NumberFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 6,
  }).format(Number(value))
}

function formatDate(value) {
  if (!value) return t('common.noExpiration')
  const datePart = value.slice(0, 10)
  const date = new Date(`${datePart}T00:00:00Z`)
  return new Intl.DateTimeFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    timeZone: 'UTC',
  }).format(date)
}
</script>

<template>
  <PageHeader
    :title="t('prices.title')"
    :description="t('prices.description')"
    :breadcrumbs="[
      t('common.breadcrumbs.home'),
      t('common.breadcrumbs.commercial'),
      t('prices.title'),
    ]"
  >
    <template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('prices.new') }}
      </button></template
    >
  </PageHeader>
  <div v-if="notice" class="alert alert-success d-flex align-items-center py-2" role="status">
    <i class="bi bi-check-circle-fill me-2"></i>{{ notice }}
  </div>
  <div v-if="serviceError && !formOpen" class="alert alert-danger py-2" role="alert">
    {{ serviceError }}
  </div>
  <div class="card app-card">
    <div class="card-body p-0">
      <div class="filters row g-3 p-3 p-lg-4">
        <div class="col-md-5">
          <SearchInput v-model="search" :placeholder="t('prices.search')" />
        </div>
        <div class="col-md-4">
          <select v-model="center" class="form-select">
            <option value="all">{{ t('prices.allCenters') }}</option>
            <option v-for="item in centros" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
        </div>
        <div class="col-md-3">
          <select v-model="status" class="form-select">
            <option value="all">{{ t('common.allStatuses') }}</option>
            <option value="active">{{ t('common.active') }}</option>
            <option value="inactive">{{ t('common.inactive') }}</option>
          </select>
        </div>
      </div>
      <LoadingSpinner v-if="cargando" :text="t('prices.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('prices.product') }}</th>
              <th>{{ t('prices.basePrice') }}</th>
              <th>{{ t('prices.discountAndFinalPrice') }}</th>
              <th>{{ t('prices.exchangeRate') }}</th>
              <th>{{ t('prices.validityAndStatus') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>

            <template v-for="group in groupedByCenter" :key="group.id">
              <tr class="center-group-row">
                <th colspan="6" scope="rowgroup">
                  <span class="center-group-icon"><i class="bi bi-building"></i></span>
                  <span>{{ group.nombre }}</span>
                  <small v-if="group.codigo" class="center-group-code">{{ group.codigo }}</small>
                  <span class="center-group-count">{{ group.items.length }}</span>
                </th>
              </tr>
              <tr v-for="item in group.items" :key="item.id">
                <td>
                  <strong class="item-name">{{ item.productoNombre }}</strong
                  ><small class="d-block text-secondary">{{ item.productoCodigo }}</small>
                </td>
                <td>
                  <div class="price-stack">
                    <div class="price-line">
                      <span class="currency-code">HNL</span>
                      <strong>{{ formatCurrency(item.precioBaseHnl, 'HNL') }}</strong>
                    </div>
                    <div class="price-line">
                      <span class="currency-code usd">USD</span>
                      <strong>{{ formatCurrency(item.precioBaseUsd, 'USD') }}</strong>
                    </div>
                  </div>
                </td>
                <td>
                  <div v-if="hasDiscount(item)" class="discount-detail">
                    <div class="discount-title">
                      <i class="bi bi-tag-fill"></i>
                      <strong>{{ item.descuentoNombre }}</strong>
                    </div>
                    <div class="discount-meta">
                      <span>{{ discountType(item) }}</span>
                      <span>{{ discountValue(item) }}</span>
                      <span>
                        {{ t('prices.discountedAmount') }}:
                        {{ formatCurrency(item.montoDescuento, item.monedaCodigo || 'HNL') }}
                      </span>
                    </div>
                  </div>
                  <div v-else class="no-discount">{{ t('prices.noDiscount') }}</div>
                  <div class="price-stack final-prices">
                    <div class="price-line">
                      <span class="currency-code">HNL</span>
                      <strong>{{ formatCurrency(item.precioFinalHnl, 'HNL') }}</strong>
                    </div>
                    <div class="price-line">
                      <span class="currency-code usd">USD</span>
                      <strong>{{ formatCurrency(item.precioFinalUsd, 'USD') }}</strong>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="exchange-rate">
                    <i class="bi bi-arrow-left-right"></i>
                    <strong>{{ formatExchangeRate(item.tasaCambio) }}</strong>
                  </div>
                  <small class="text-secondary">{{ t('prices.rateUsed') }}</small>
                </td>
                <td>
                  <div class="validity-period">
                    <div>
                      <i class="bi bi-calendar-event"></i>
                      {{ formatDate(item.fechaInicio) }}
                    </div>
                    <div>
                      <i class="bi bi-calendar-check"></i>
                      {{ formatDate(item.fechaFin) }}
                    </div>
                  </div>
                  <StatusBadge class="mt-2" :active="item.activo" />
                </td>
                <td class="text-end text-nowrap">
                  <button
                    class="btn btn-action btn-sm me-1"
                    :title="t('common.edit')"
                    @click="edit(item)"
                  >
                    <i class="bi bi-pencil"></i></button
                  ><button
                    class="btn btn-action btn-sm"
                    :title="item.activo ? t('common.deactivate') : t('common.activate')"
                    @click="askStatus(item)"
                  >
                    <i
                      class="bi"
                      :class="
                        item.activo ? 'bi-toggle-on text-success' : 'bi-toggle-off text-secondary'
                      "
                    ></i>
                  </button>
                </td>
              </tr>
            </template>
            <tr v-if="!filtered.length">
              <td colspan="6" class="empty-state text-center">
                <i class="bi bi-search d-block"></i>{{ t('prices.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: precios.length })
        }}</small>
        <nav :aria-label="t('common.page')">
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item disabled">
              <button class="page-link">{{ t('common.previous') }}</button>
            </li>
            <li class="page-item active"><button class="page-link">1</button></li>
            <li class="page-item disabled">
              <button class="page-link">{{ t('common.next') }}</button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
  <BaseModal
    :show="formOpen"
    :title="editing ? t('prices.edit') : t('prices.new')"
    @close="!guardando && (formOpen = false)"
    ><div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <PrecioForm
      :precio-item="editing"
      :productos="productos"
      :centros="centros"
      :monedas="monedas"
      :saving="guardando"
      @submit="save"
    /><template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="precio-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('prices.create') }}
      </button></template
    ></BaseModal
  >
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t(selected.activo ? 'prices.confirmDeactivate' : 'prices.confirmActivate', {
            name: selected.productoNombre,
          })
        : ''
    "
    :confirm-text="selected?.activo ? t('common.deactivate') : t('common.activate')"
    :confirm-class="selected?.activo ? 'btn-danger' : 'btn-success'"
    @close="confirmOpen = false"
    @confirm="toggleStatus"
  />
</template>

<style scoped>
.filters {
  border-bottom: 1px solid var(--app-border);
}
.item-name {
  color: #2b3548;
  font-size: 0.88rem;
}
.center-group-row th {
  padding: 0.75rem 1rem;
  color: #34425b;
  background: #f1f4f9;
  border-top: 1px solid var(--app-border);
  font-size: 0.86rem;
}
.center-group-icon {
  display: inline-grid;
  width: 28px;
  height: 28px;
  margin-right: 0.55rem;
  place-items: center;
  color: #3157d5;
  background: #e2e9ff;
  border-radius: 0.45rem;
}
.center-group-code {
  margin-left: 0.5rem;
  color: #7a8598;
}
.center-group-count {
  float: right;
  min-width: 28px;
  padding: 0.2rem 0.5rem;
  text-align: center;
  color: #536078;
  background: #fff;
  border: 1px solid #dce1e9;
  border-radius: 999px;
}
.currency-code {
  display: inline-block;
  padding: 0.28rem 0.5rem;
  border-radius: 0.4rem;
  color: #42506a;
  background: #eef1f5;
  font-family: ui-monospace, monospace;
  font-size: 0.78rem;
  font-weight: 700;
}
.currency-code.usd {
  color: #146c43;
  background: #e7f5ed;
}
.price-stack {
  display: grid;
  min-width: 165px;
  gap: 0.45rem;
}
.price-line {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.price-line strong {
  color: #273249;
  white-space: nowrap;
}
.final-prices {
  padding-top: 0.6rem;
  margin-top: 0.6rem;
  border-top: 1px dashed #dce1e9;
}
.final-prices strong {
  color: #146c43;
}
.discount-detail {
  min-width: 225px;
  padding: 0.65rem;
  color: #704d00;
  background: #fff8e5;
  border: 1px solid #f2dfa4;
  border-radius: 0.55rem;
}
.discount-title {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.discount-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 0.75rem;
  margin-top: 0.35rem;
  font-size: 0.75rem;
}
.no-discount {
  color: #7a8598;
  font-size: 0.8rem;
}
.exchange-rate {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  color: #3157d5;
  white-space: nowrap;
}
.validity-period {
  display: grid;
  gap: 0.25rem;
  color: #536078;
  font-size: 0.8rem;
  white-space: nowrap;
}
.validity-period i {
  width: 18px;
  margin-right: 0.25rem;
  color: #7a8598;
}
@media (max-width: 991.98px) {
  .table {
    min-width: 1080px;
  }
}
.btn-action {
  width: 34px;
  height: 34px;
  padding: 0;
  border: 1px solid var(--app-border);
  color: #536078;
  background: white;
}
.btn-action:hover {
  color: #3157d5;
  background: #f1f4ff;
  border-color: #cbd5f6;
}
.btn-action .bi-toggle-on,
.btn-action .bi-toggle-off {
  font-size: 1.15rem;
}
.empty-state {
  padding: 3.5rem 1rem !important;
  color: #8b94a4;
}
.empty-state i {
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}
.page-link {
  color: #536078;
}
.page-item.active .page-link {
  background: #3157d5;
  border-color: #3157d5;
}
</style>
