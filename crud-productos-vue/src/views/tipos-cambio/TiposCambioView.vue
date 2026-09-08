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
  actualizarTipoCambio,
  cambiarEstadoTipoCambio,
  crearTipoCambio,
  listarTiposCambio,
  obtenerTipoCambio,
} from '@/services/tipoCambioService'
import TipoCambioForm from './TipoCambioForm.vue'

const { t, locale } = useI18n()
const tipos = ref([])
const monedas = ref(MONEDAS)
const cargando = ref(false)
const guardando = ref(false)
const search = ref('')
const status = ref('all')
const formOpen = ref(false)
const editing = ref(null)
const confirmOpen = ref(false)
const selected = ref(null)
const notice = ref('')
const serviceError = ref('')

const filtered = computed(() => {
  return tipos.value.filter((item) => {
    const term = search.value.trim().toLowerCase()
    const origen = (item.monedaOrigenCodigo || '').toLowerCase()
    const destino = (item.monedaDestinoCodigo || '').toLowerCase()
    const matchesText = !term || origen.includes(term) || destino.includes(term)
    const matchesStatus = status.value === 'all' || item.activo === (status.value === 'active')
    return matchesText && matchesStatus
  })
})

onMounted(load)
watch(locale, load)

function getErrorMessage(error) {
  if (error.message) return error.message
  return t('exchangeRates.loadError')
}

async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    tipos.value = await listarTiposCambio(locale.value)
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
    editing.value = await obtenerTipoCambio(item.id, locale.value)
    formOpen.value = true
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function showNotice(key) {
  notice.value = t(key)
  setTimeout(() => {
    notice.value = ''
  }, 3000)
}

async function save(data) {
  if (guardando.value) return
  guardando.value = true
  serviceError.value = ''
  try {
    const wasEditing = Boolean(editing.value)
    if (wasEditing) await actualizarTipoCambio(editing.value.id, data, locale.value)
    else await crearTipoCambio(data, locale.value)
    formOpen.value = false
    await load()
    showNotice(wasEditing ? 'exchangeRates.updated' : 'exchangeRates.created')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
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
    const activating = !selected.value.activo
    await cambiarEstadoTipoCambio(selected.value.id)
    confirmOpen.value = false
    await load()
    showNotice(activating ? 'exchangeRates.activated' : 'exchangeRates.deactivated')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function formatRate(value) {
  return new Intl.NumberFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    minimumFractionDigits: 8,
    maximumFractionDigits: 8,
  }).format(value)
}

function formatExample(item) {
  const resultado = 100 * Number(item.tasa)
  const formatted = new Intl.NumberFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    maximumFractionDigits: 8,
  }).format(resultado)
  return t('exchangeRates.tableExample', {
    origin: item.monedaOrigenCodigo,
    destination: item.monedaDestinoCodigo,
    result: formatted,
  })
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
    :title="t('exchangeRates.title')"
    :description="t('exchangeRates.description')"
    :breadcrumbs="[
      t('common.breadcrumbs.home'),
      t('common.breadcrumbs.configuration'),
      t('exchangeRates.title'),
    ]"
  >
    <template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('exchangeRates.new') }}
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
        <div class="col-md-7 col-lg-5">
          <SearchInput v-model="search" :placeholder="t('exchangeRates.search')" />
        </div>
        <div class="col-md-5 col-lg-3 ms-lg-auto">
          <select v-model="status" class="form-select">
            <option value="all">{{ t('common.allStatuses') }}</option>
            <option value="active">{{ t('common.active') }}</option>
            <option value="inactive">{{ t('common.inactive') }}</option>
          </select>
        </div>
      </div>
      <LoadingSpinner v-if="cargando" :text="t('exchangeRates.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('exchangeRates.origin') }}</th>
              <th>{{ t('exchangeRates.destination') }}</th>
              <th>{{ t('exchangeRates.rate') }}</th>
              <th>{{ t('common.startDate') }}</th>
              <th>{{ t('common.endDate') }}</th>
              <th>{{ t('common.status') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filtered" :key="item.id">
              <td>
                <span class="currency-code">{{ item.monedaOrigenCodigo }}</span
                ><small class="d-block text-secondary">{{ item.monedaOrigenNombre }}</small>
              </td>
              <td>
                <span class="currency-code">{{ item.monedaDestinoCodigo }}</span
                ><small class="d-block text-secondary">{{ item.monedaDestinoNombre }}</small>
              </td>
              <td>
                <strong>{{ formatRate(item.tasa) }}</strong>
                <small class="d-block text-secondary"
                  >{{ item.monedaOrigenCodigo }} → {{ item.monedaDestinoCodigo }}</small
                >
                <small class="d-block text-secondary">{{ formatExample(item) }}</small>
              </td>
              <td class="text-nowrap">{{ formatDate(item.fechaInicio) }}</td>
              <td class="text-nowrap">{{ formatDate(item.fechaFin) }}</td>
              <td><StatusBadge :active="item.activo" /></td>
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
            <tr v-if="!filtered.length">
              <td colspan="7" class="empty-state text-center">
                <i class="bi bi-search d-block"></i>{{ t('exchangeRates.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: tipos.length })
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
    :title="editing ? t('exchangeRates.edit') : t('exchangeRates.new')"
    @close="!guardando && (formOpen = false)"
    ><div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <TipoCambioForm
      :tipo-cambio="editing"
      :monedas="monedas"
      :saving="guardando"
      @submit="save"
    /><template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="tipo-cambio-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('exchangeRates.create') }}
      </button></template
    ></BaseModal
  >
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t(selected.activo ? 'exchangeRates.confirmDeactivate' : 'exchangeRates.confirmActivate', {
            origin: selected.monedaOrigenCodigo,
            destination: selected.monedaDestinoCodigo,
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
