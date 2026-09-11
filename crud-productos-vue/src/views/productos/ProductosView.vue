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
  actualizarProducto,
  cambiarEstadoProducto,
  crearProducto,
  listarCategoriasProducto,
  listarMarcasProducto,
  listarProductos,
  obtenerProducto,
} from '@/services/productoService'
import ProductoForm from './ProductoForm.vue'

const { t, locale } = useI18n()
const productos = ref([])
const categorias = ref([])
const marcas = ref([])
const cargando = ref(false)
const guardando = ref(false)
const search = ref('')
const status = ref('all')
const category = ref('all')
const formOpen = ref(false)
const editing = ref(null)
const confirmOpen = ref(false)
const selected = ref(null)
const notice = ref('')
const serviceError = ref('')

const filtered = computed(() => {
  return productos.value.filter((item) => {
    const term = search.value.trim().toLowerCase()
    const codigo = (item.codigo || '').toLowerCase()
    const sku = (item.sku || '').toLowerCase()
    const barcode = (item.codigoBarras || '').toLowerCase()
    const nombre = (item.nombre || '').toLowerCase()
    const matchesText =
      !term ||
      codigo.includes(term) ||
      sku.includes(term) ||
      barcode.includes(term) ||
      nombre.includes(term)
    const matchesStatus = status.value === 'all' || item.activo === (status.value === 'active')
    const matchesCategory = category.value === 'all' || item.categoriaId === Number(category.value)
    return matchesText && matchesStatus && matchesCategory
  })
})

const existingCodes = computed(() =>
  productos.value.filter((item) => item.id !== editing.value?.id).map((item) => item.codigo),
)
const existingSkus = computed(() =>
  productos.value.filter((item) => item.id !== editing.value?.id).map((item) => item.sku),
)
const existingBarcodes = computed(() =>
  productos.value
    .filter((item) => item.id !== editing.value?.id && item.codigoBarras)
    .map((item) => item.codigoBarras),
)

onMounted(load)
watch(locale, load)

function getErrorMessage(error) {
  if (error.message) return error.message
  return t('products.loadError')
}

async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    const respuestas = await Promise.all([
      listarProductos(locale.value),
      listarCategoriasProducto(locale.value),
      listarMarcasProducto(locale.value),
    ])
    productos.value = respuestas[0]
    categorias.value = respuestas[1]
    marcas.value = respuestas[2]
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
      obtenerProducto(item.id, 'es'),
      obtenerProducto(item.id, 'en'),
    ])
    const productoEs = respuestas[0]
    const productoEn = respuestas[1]
    editing.value = {
      id: item.id,
      codigo: productoEs.codigo || productoEn.codigo || item.codigo,
      sku: productoEs.sku || productoEn.sku || item.sku,
      codigoBarras: productoEs.codigoBarras || productoEn.codigoBarras || '',
      categoriaId: productoEs.categoriaId ?? productoEn.categoriaId ?? item.categoriaId,
      marcaId: productoEs.marcaId ?? productoEn.marcaId ?? item.marcaId,
      activo: productoEs.activo ?? productoEn.activo ?? item.activo,
      traducciones: {
        es: { nombre: productoEs.nombre || '', descripcion: productoEs.descripcion || '' },
        en: { nombre: productoEn.nombre || '', descripcion: productoEn.descripcion || '' },
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
    if (wasEditing) await actualizarProducto(editing.value.id, data, locale.value)
    else await crearProducto(data, locale.value)
    formOpen.value = false
    await load()
    showNotice(wasEditing ? 'products.updated' : 'products.created')
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
    await cambiarEstadoProducto(selected.value.id)
    confirmOpen.value = false
    await load()
    showNotice(activating ? 'products.activated' : 'products.deactivated')
  } catch (error) {
    serviceError.value = getErrorMessage(error)
  } finally {
    guardando.value = false
  }
}
</script>

<template>
  <PageHeader
    :title="t('products.title')"
    :description="t('products.description')"
    :breadcrumbs="[
      t('common.breadcrumbs.home'),
      t('common.breadcrumbs.catalog'),
      t('products.title'),
    ]"
  >
    <template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('products.new') }}
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
        <div class="col-lg-5">
          <SearchInput v-model="search" :placeholder="t('products.search')" />
        </div>
        <div class="col-sm-6 col-lg-3">
          <select v-model="category" class="form-select">
            <option value="all">{{ t('products.allCategories') }}</option>
            <option v-for="item in categorias" :key="item.id" :value="item.id">
              {{ item.nombre }}
            </option>
          </select>
        </div>
        <div class="col-sm-6 col-lg-3 ms-lg-auto">
          <select v-model="status" class="form-select">
            <option value="all">{{ t('common.allStatuses') }}</option>
            <option value="active">{{ t('common.active') }}</option>
            <option value="inactive">{{ t('common.inactive') }}</option>
          </select>
        </div>
      </div>
      <LoadingSpinner v-if="cargando" :text="t('products.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('common.code') }}</th>
              <th>SKU</th>
              <th>{{ t('common.name') }}</th>
              <th>{{ t('products.category') }}</th>
              <th>{{ t('products.brand') }}</th>
              <th>{{ t('common.status') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filtered" :key="item.id">
              <td>
                <span class="code-label">{{ item.codigo }}</span>
              </td>
              <td class="text-nowrap">{{ item.sku }}</td>
              <td>
                <strong class="product-name">{{ item.nombre }}</strong
                ><small class="d-block text-secondary">{{
                  item.codigoBarras || t('products.noBarcode')
                }}</small>
              </td>
              <td>{{ item.categoriaNombre }}</td>
              <td>{{ item.marcaNombre || t('products.noBrand') }}</td>
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
                <i class="bi bi-search d-block"></i>{{ t('products.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: productos.length })
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
    :title="editing ? t('products.edit') : t('products.new')"
    @close="!guardando && (formOpen = false)"
    ><div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <ProductoForm
      :producto="editing"
      :categorias="categorias"
      :marcas="marcas"
      :existing-codes="existingCodes"
      :existing-skus="existingSkus"
      :existing-barcodes="existingBarcodes"
      :saving="guardando"
      @submit="save"
    /><template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="producto-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('products.create') }}
      </button></template
    ></BaseModal
  >
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t(selected.activo ? 'products.confirmDeactivate' : 'products.confirmActivate', {
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
.product-name {
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
