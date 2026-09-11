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
  actualizarMarca,
  cambiarEstadoMarca,
  crearMarca,
  listarMarcas,
  obtenerMarca,
} from '@/services/marcaService'
import MarcaForm from './MarcaForm.vue'

const { t, locale } = useI18n()
const marcas = ref([]),
  cargando = ref(false),
  guardando = ref(false)
const search = ref(''),
  status = ref('all'),
  formOpen = ref(false),
  editing = ref(null)
const confirmOpen = ref(false),
  selected = ref(null),
  notice = ref(''),
  serviceError = ref('')

const filtered = computed(() =>
  marcas.value.filter((item) => {
    const term = search.value.trim().toLowerCase()
    return (
      (!term || (item.nombre || '').toLowerCase().includes(term)) &&
      (status.value === 'all' || item.activo === (status.value === 'active'))
    )
  }),
)

onMounted(load)
watch(locale, load)

const errorMessage = (error) =>
  error.response?.data?.message || error.response?.data?.detail || t('brands.loadError')
async function load() {
  cargando.value = true
  serviceError.value = ''
  try {
    marcas.value = await listarMarcas(locale.value)
  } catch (error) {
    serviceError.value = errorMessage(error)
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
    const [es, en] = await Promise.all([obtenerMarca(item.id, 'es'), obtenerMarca(item.id, 'en')])
    editing.value = {
      id: item.id,
      activo: es.activo ?? en.activo ?? item.activo,
      traducciones: { es: { nombre: es.nombre || '' }, en: { nombre: en.nombre || '' } },
    }
    formOpen.value = true
  } catch (error) {
    serviceError.value = errorMessage(error)
  } finally {
    guardando.value = false
  }
}
function showNotice(key) {
  notice.value = t(key)
  setTimeout(() => (notice.value = ''), 3000)
}
async function save(data) {
  guardando.value = true
  serviceError.value = ''
  try {
    const wasEditing = Boolean(editing.value)
    if (wasEditing) await actualizarMarca(editing.value.id, data, locale.value)
    else await crearMarca(data, locale.value)
    formOpen.value = false
    await load()
    showNotice(wasEditing ? 'brands.updated' : 'brands.created')
  } catch (error) {
    serviceError.value = errorMessage(error)
  } finally {
    guardando.value = false
  }
}
function askStatus(item) {
  selected.value = item
  confirmOpen.value = true
}
async function toggleStatus() {
  guardando.value = true
  serviceError.value = ''
  try {
    const activating = !selected.value.activo
    await cambiarEstadoMarca(selected.value.id)
    confirmOpen.value = false
    await load()
    showNotice(activating ? 'brands.activated' : 'brands.deactivated')
  } catch (error) {
    serviceError.value = errorMessage(error)
  } finally {
    guardando.value = false
  }
}
</script>

<template>
  <PageHeader
    :title="t('brands.title')"
    :description="t('brands.description')"
    :breadcrumbs="[
      t('common.breadcrumbs.home'),
      t('common.breadcrumbs.catalog'),
      t('brands.title'),
    ]"
  >
    <template #actions
      ><button class="btn btn-primary" @click="create">
        <i class="bi bi-plus-lg me-2"></i>{{ t('brands.new') }}
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
          <SearchInput v-model="search" :placeholder="t('brands.search')" />
        </div>
        <div class="col-md-5 col-lg-3 ms-lg-auto">
          <select v-model="status" class="form-select">
            <option value="all">{{ t('common.allStatuses') }}</option>
            <option value="active">{{ t('common.active') }}</option>
            <option value="inactive">{{ t('common.inactive') }}</option>
          </select>
        </div>
      </div>
      <LoadingSpinner v-if="cargando" :text="t('brands.loading')" />
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>{{ t('common.name') }}</th>
              <th>{{ t('common.status') }}</th>
              <th class="text-end">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filtered" :key="item.id">
              <td>
                <strong class="brand-name">{{ item.nombre }}</strong>
              </td>
              <td><StatusBadge :active="item.activo" /></td>
              <td class="text-end text-nowrap">
                <button
                  class="btn btn-action btn-sm me-1"
                  :title="t('common.edit')"
                  @click="edit(item)"
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button
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
              <td colspan="3" class="empty-state text-center">
                <i class="bi bi-search d-block"></i>{{ t('brands.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        class="d-flex flex-wrap justify-content-between align-items-center gap-2 p-3 px-lg-4 border-top"
      >
        <small class="text-secondary">{{
          t('common.records', { shown: filtered.length, total: marcas.length })
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
    :title="editing ? t('brands.edit') : t('brands.new')"
    @close="!guardando && (formOpen = false)"
  >
    <div v-if="serviceError" class="alert alert-danger py-2">{{ serviceError }}</div>
    <MarcaForm :marca="editing" :saving="guardando" @submit="save" />
    <template #footer
      ><button class="btn btn-light" :disabled="guardando" @click="formOpen = false">
        {{ t('common.cancel') }}</button
      ><button type="submit" form="marca-form" class="btn btn-primary" :disabled="guardando">
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span
        >{{ editing ? t('common.saveChanges') : t('brands.create') }}
      </button></template
    >
  </BaseModal>
  <ConfirmModal
    :show="confirmOpen"
    :loading="guardando"
    :message="
      selected
        ? t(selected.activo ? 'brands.confirmDeactivate' : 'brands.confirmActivate', {
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
.brand-name {
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
