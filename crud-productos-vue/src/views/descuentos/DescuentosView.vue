<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import {
  actualizarDescuento,
  cambiarEstadoDescuento,
  crearDescuento,
  listarCentrosDescuento,
  listarDescuentos,
  listarProductosDescuento,
  listarTiposDescuento,
  obtenerDescuento,
} from '@/services/descuentoService'
import DescuentoForm from './DescuentoForm.vue'

const { t, locale } = useI18n()
const descuentos = ref([]),
  centros = ref([]),
  tipos = ref([]),
  productos = ref([])
const cargando = ref(false),
  guardando = ref(false),
  search = ref(''),
  center = ref('all'),
  status = ref('all')
const formOpen = ref(false),
  editing = ref(null),
  confirmOpen = ref(false),
  selected = ref(null),
  notice = ref(''),
  serviceError = ref('')

const filtered = computed(() =>
  descuentos.value.filter((item) => {
    if (item.tipoDescuentoCodigo !== 'PORCENTAJE') return false

    const term = search.value.trim().toLowerCase()
    const matchesText =
      !term ||
      (item.codigo || '').toLowerCase().includes(term) ||
      (item.nombre || '').toLowerCase().includes(term)
    const matchesCenter =
      center.value === 'all' || item.centroDistribucionId === Number(center.value)
    const matchesStatus = status.value === 'all' || item.activo === (status.value === 'active')
    return matchesText && matchesCenter && matchesStatus
  }),
)

onMounted(load)
watch(locale, load)

function getErrorMessage(error) {
  if (error.message) return error.message
  return t('discounts.loadError')
}

async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    const respuestas = await Promise.all([
      listarDescuentos(locale.value),
      listarCentrosDescuento(locale.value),
      listarTiposDescuento(locale.value),
      listarProductosDescuento(locale.value),
    ])
    descuentos.value = respuestas[0]
    centros.value = respuestas[1]
    tipos.value = respuestas[2].filter((item) => item.codigo === 'PORCENTAJE')
    productos.value = respuestas[3]
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
    const respuestas = await Promise.all([
      obtenerDescuento(item.id, 'es'),
      obtenerDescuento(item.id, 'en'),
    ])
    const es = respuestas[0],
      en = respuestas[1]
    editing.value = {
      id: item.id,
      codigo: es.codigo || en.codigo,
      centroDistribucionId: es.centroDistribucionId ?? en.centroDistribucionId,
      tipoDescuentoId: es.tipoDescuentoId ?? en.tipoDescuentoId,
      valor: es.valor ?? en.valor,
      monedaId: es.monedaId ?? en.monedaId,
      fechaInicio: es.fechaInicio || en.fechaInicio,
      fechaFin: es.fechaFin || en.fechaFin,
      activo: es.activo ?? en.activo,
      productos: es.productos || en.productos || [],
      traducciones: {
        es: { nombre: es.nombre || '', descripcion: es.descripcion || '' },
        en: { nombre: en.nombre || '', descripcion: en.descripcion || '' },
      },
    }
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
    if (wasEditing) await actualizarDescuento(editing.value.id, data, locale.value)
    else await crearDescuento(data, locale.value)
    formOpen.value = false
    await load()
    showNotice(wasEditing ? 'discounts.updated' : 'discounts.created')
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
    await cambiarEstadoDescuento(selected.value.id)
    confirmOpen.value = false
    await load()
    showNotice(activating ? 'discounts.activated' : 'discounts.deactivated')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function formatValue(item) {
  return `${Number(item.valor).toLocaleString(locale.value === 'en' ? 'en-US' : 'es-HN')}%`
}

function formatDate(value) {
  if (!value) return t('common.noExpiration')
  const date = new Date(`${value.slice(0, 10)}T00:00:00Z`)
  return new Intl.DateTimeFormat(locale.value === 'en' ? 'en-US' : 'es-HN', {
    timeZone: 'UTC',
  }).format(date)
}
</script>

<template>
  <PageHeader
    :title="t('discounts.title')"
    :description="t('discounts.description')"
    :breadcrumbs="[
      t('common.breadcrumbs.home'),
      t('common.breadcrumbs.commercial'),
      t('discounts.title'),
    ]"
    ><template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('discounts.new') }}
      </button></template
    ></PageHeader
  >
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
          <SearchInput v-model="search" :placeholder="t('discounts.search')" />
        </div>
        <div class="col-md-4">
          <select v-model="center" class="form-select">
            <option value="all">{{ t('discounts.allCenters') }}</option>
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
      <LoadingSpinner v-if="cargando" :text="t('discounts.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('common.code') }}</th>
              <th>{{ t('common.name') }}</th>
              <th>{{ t('discounts.center') }}</th>
              <th>{{ t('discounts.value') }}</th>
              <th>{{ t('discounts.validity') }}</th>
              <th>{{ t('discounts.products') }}</th>
              <th>{{ t('common.status') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filtered" :key="item.id">
              <td>
                <span class="code-label">{{ item.codigo }}</span>
              </td>
              <td>
                <strong class="discount-name">{{ item.nombre }}</strong
                ><small class="d-block text-secondary">{{ item.descripcion || '—' }}</small>
              </td>
              <td>{{ item.centroDistribucionNombre }}</td>
              <td>
                <strong>{{ formatValue(item) }}</strong>
              </td>
              <td class="text-nowrap">
                <small
                  >{{ formatDate(item.fechaInicio) }}<br /><span class="text-secondary"
                    >{{ t('discounts.until') }} {{ formatDate(item.fechaFin) }}</span
                  ></small
                >
              </td>
              <td>
                <span class="badge text-bg-light border">{{
                  t('discounts.productCount', { count: item.productos?.length || 0 })
                }}</span>
              </td>
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
              <td colspan="8" class="empty-state text-center">
                <i class="bi bi-search d-block"></i>{{ t('discounts.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: descuentos.length })
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
    :title="editing ? t('discounts.edit') : t('discounts.new')"
    @close="!guardando && (formOpen = false)"
    ><div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <DescuentoForm
      :descuento="editing"
      :centros="centros"
      :tipos="tipos"
      :productos="productos"
      :saving="guardando"
      @submit="save"
    /><template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="descuento-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('discounts.create') }}
      </button></template
    ></BaseModal
  >
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t(selected.activo ? 'discounts.confirmDeactivate' : 'discounts.confirmActivate', {
            name: selected.nombre,
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
.code-label {
  display: inline-block;
  padding: 0.28rem 0.5rem;
  border-radius: 0.4rem;
  color: #42506a;
  background: #eef1f5;
  font-family: ui-monospace, monospace;
  font-size: 0.78rem;
  font-weight: 700;
}
.discount-name {
  color: #2b3548;
  font-size: 0.88rem;
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
