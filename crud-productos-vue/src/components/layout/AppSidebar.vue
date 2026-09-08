<script setup>
import { useI18n } from 'vue-i18n'
defineProps({ open: { type: Boolean, default: false } })
defineEmits(['close'])
const { t } = useI18n()
const items = [
  ['menu.dashboard', 'bi-grid-1x2', '/dashboard'],
  ['menu.categories', 'bi-tags', '/categorias'],
  ['menu.brands', 'bi-bookmark', '/marcas'],
  ['menu.distributionCenters', 'bi-building', '/centros-distribucion'],
  ['menu.products', 'bi-box-seam', '/productos'],
  ['menu.inventory', 'bi-clipboard-data', '/inventario'],
  ['menu.prices', 'bi-cash-coin', '/precios'],
  ['menu.discounts', 'bi-percent', '/descuentos'],
  ['menu.exchangeRates', 'bi-graph-up-arrow', '/tipos-cambio'],
]
</script>
<template>
  <aside class="sidebar" :class="{ show: open }">
    <div class="sidebar-brand">
      <span class="brand-mark"><i class="bi bi-boxes"></i></span>
      <div>
        <strong>PowerInventarios</strong><small>{{ t('common.administration') }}</small>
      </div>
      <button
        class="btn-close btn-close-white ms-auto d-lg-none"
        :aria-label="t('common.closeMenu')"
        @click="$emit('close')"
      ></button>
    </div>
    <div class="sidebar-label">{{ t('common.mainMenu') }}</div>
    <nav class="sidebar-nav">
      <template v-for="item in items" :key="item[0]"
        ><RouterLink v-if="item[2]" :to="item[2]" class="sidebar-link" @click="$emit('close')"
          ><i class="bi" :class="item[1]"></i><span>{{ t(item[0]) }}</span></RouterLink
        ><span v-else class="sidebar-link disabled" :title="t('common.availableSoon')"
          ><i class="bi" :class="item[1]"></i><span>{{ t(item[0]) }}</span
          ><small class="ms-auto">{{ t('common.soon') }}</small></span
        ></template
      >
    </nav>
  </aside>
  <div v-if="open" class="sidebar-backdrop d-lg-none" @click="$emit('close')"></div>
</template>
<style scoped>
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 1040;
  width: var(--app-sidebar-width);
  overflow-y: auto;
  background: var(--app-sidebar-bg);
  color: #fff;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 76px;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.brand-mark {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #4f6ee8;
  font-size: 1.25rem;
}
.sidebar-brand strong,
.sidebar-brand small {
  display: block;
}
.sidebar-brand small {
  color: #9ba7bd;
  font-size: 0.72rem;
}
.sidebar-label {
  padding: 1.5rem 1.25rem 0.55rem;
  color: #77849d;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}
.sidebar-nav {
  padding: 0 0.75rem 1.5rem;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0.18rem 0;
  padding: 0.7rem 0.85rem;
  border-radius: 0.55rem;
  color: #b9c3d4;
  text-decoration: none;
  transition: 0.18s;
}
.sidebar-link i {
  width: 21px;
}
.sidebar-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.07);
}
.sidebar-link.router-link-active {
  color: white;
  background: #3157d5;
}
.sidebar-link.disabled {
  cursor: default;
  opacity: 0.6;
}
.sidebar-link.disabled:hover {
  color: #b9c3d4;
  background: transparent;
}
.sidebar-link small {
  color: #7e8ba4;
  font-size: 0.62rem;
  text-transform: uppercase;
}
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1035;
  background: rgba(15, 23, 42, 0.55);
}
@media (max-width: 991.98px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.25s;
  }
  .sidebar.show {
    transform: translateX(0);
  }
}
</style>
