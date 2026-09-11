<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import {
  actualizarInventario,
  crearInventario,
  eliminarInventario,
  listarCentrosInventario,
  listarInventario,
  listarProductosInventario,
  obtenerInventario,
} from '@/services/inventarioService'
import InventarioForm from './InventarioForm.vue'

const { t, locale } = useI18n()
const inventarios = ref([])
const productos = ref([])
const centros = ref([])
const cargando = ref(false)
const guardando = ref(false)
const search = ref('')
const center = ref('all')
const formOpen = ref(false)
const editing = ref(null)
const confirmOpen = ref(false)
const selected = ref(null)
const notice = ref('')
const serviceError = ref('')

const filtered = computed(() => {
  return inventarios.value.filter((item) => {
    const term = search.value.trim().toLowerCase()
    const codigo = (item.productoCodigo || '').toLowerCase()
    const nombre = (item.productoNombre || '').toLowerCase()
    const matchesText = !term || codigo.includes(term) || nombre.includes(term)
    const matchesCenter =
      center.value === 'all' || item.centroDistribucionId === Number(center.value)
    return matchesText && matchesCenter
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

const existingCombinations = computed(() => {
  const combinations = []
  inventarios.value.forEach((item) => {
    if (item.id !== editing.value?.id)
      combinations.push(`${item.productoId}-${item.centroDistribucionId}`)
  })
  return combinations
})

onMounted(load)
watch(locale, load)

function getErrorMessage(error) {
  if (error.message) return error.message
  return t('inventory.loadError')
}

async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    const respuestas = await Promise.all([
      listarInventario(locale.value),
      listarProductosInventario(locale.value),
      listarCentrosInventario(locale.value),
    ])
    inventarios.value = respuestas[0]
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
    editing.value = await obtenerInventario(item.id, locale.value)
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
    if (wasEditing) await actualizarInventario(editing.value.id, data, locale.value)
    else await crearInventario(data, locale.value)
    formOpen.value = false
    await load()
    showNotice(wasEditing ? 'inventory.updated' : 'inventory.created')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function askDelete(item) {
  selected.value = item
  confirmOpen.value = true
}

async function remove() {
  if (guardando.value) return
  guardando.value = true
  serviceError.value = ''
  try {
    await eliminarInventario(selected.value.id)
    confirmOpen.value = false
    await load()
    showNotice('inventory.deleted')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}

function isLowStock(item) {
  return item.cantidadMinima != null && item.cantidadDisponible <= item.cantidadMinima
}

function formatDate(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat(locale.value === 'en' ? 'en-US' : 'es-NI', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}
</script>

<template>
  <PageHeader
    :title="t('inventory.title')"
    :description="t('inventory.description')"
    :breadcrumbs="[t('common.breadcrumbs.home'), t('inventory.title')]"
  >
    <template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('inventory.new') }}
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
          <SearchInput v-model="search" :placeholder="t('inventory.search')" />
        </div>
        <div class="col-md-5 col-lg-4 ms-lg-auto">
          <select v-model="center" class="form-select">
            <option value="all">{{ t('inventory.allCenters') }}</option>
            <option v-for="item in centros" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
        </div>
      </div>
      <LoadingSpinner v-if="cargando" :text="t('inventory.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('inventory.product') }}</th>
              <th>{{ t('inventory.available') }}</th>
              <th>{{ t('inventory.reserved') }}</th>
              <th>{{ t('inventory.minimum') }}</th>
              <th>{{ t('inventory.maximum') }}</th>
              <th>{{ t('inventory.lastUpdate') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="group in groupedByCenter" :key="group.id">
              <tr class="center-group-row">
                <th colspan="7" scope="rowgroup">
                  <span class="center-group-icon"><i class="bi bi-building"></i></span>
                  <span>{{ group.nombre }}</span>
                  <small v-if="group.codigo" class="center-group-code">{{ group.codigo }}</small>
                  <span class="center-group-count">{{ group.items.length }}</span>
                </th>
              </tr>
              <tr
                v-for="item in group.items"
                :key="item.id"
                :class="{ 'table-warning': isLowStock(item) }"
              >
                <td>
                  <strong class="item-name">{{ item.productoNombre }}</strong
                  ><small class="d-block text-secondary">{{ item.productoCodigo }}</small>
                </td>
                <td>
                  <strong>{{ item.cantidadDisponible }}</strong
                  ><span v-if="isLowStock(item)" class="badge text-bg-warning ms-2"
                    ><i class="bi bi-exclamation-triangle me-1"></i
                    >{{ t('inventory.lowStock') }}</span
                  >
                </td>
                <td>{{ item.cantidadReservada }}</td>
                <td>{{ item.cantidadMinima ?? '—' }}</td>
                <td>{{ item.cantidadMaxima ?? '—' }}</td>
                <td class="text-nowrap">
                  <small>{{ formatDate(item.fechaActualizacion) }}</small>
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
                    :title="t('common.delete')"
                    @click="askDelete(item)"
                  >
                    <i class="bi bi-trash text-danger"></i>
                  </button>
                </td>
              </tr>
            </template>
            <tr v-if="!filtered.length">
              <td colspan="7" class="empty-state text-center">
                <i class="bi bi-search d-block"></i>{{ t('inventory.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: inventarios.length })
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
    :title="editing ? t('inventory.edit') : t('inventory.new')"
    @close="!guardando && (formOpen = false)"
    ><div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <InventarioForm
      :inventario="editing"
      :productos="productos"
      :centros="centros"
      :existing-combinations="existingCombinations"
      :saving="guardando"
      @submit="save"
    /><template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="inventario-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('inventory.create') }}
      </button></template
    ></BaseModal
  >
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t('inventory.confirmDelete', {
            product: selected.productoNombre,
            center: selected.centroDistribucionNombre,
          })
        : ''
    "
    :confirm-text="t('common.delete')"
    confirm-class="btn-danger"
    @close="confirmOpen = false"
    @confirm="remove"
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
.table-warning {
  --bs-table-bg: #fff9e8;
  --bs-table-hover-bg: #fff4d5;
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
