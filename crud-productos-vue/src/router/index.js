import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import CategoriasView from '@/views/categorias/CategoriasView.vue'
import MarcasView from '@/views/marcas/MarcasView.vue'
import CentrosDistribucionView from '@/views/centros-distribucion/CentrosDistribucionView.vue'
import TiposCambioView from '@/views/tipos-cambio/TiposCambioView.vue'
import ProductosView from '@/views/productos/ProductosView.vue'
import InventarioView from '@/views/inventario/InventarioView.vue'
import PreciosView from '@/views/precios/PreciosView.vue'
import DescuentosView from '@/views/descuentos/DescuentosView.vue'

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: DashboardView, meta: { titleKey: 'menu.dashboard' } },
    { path: '/categorias', component: CategoriasView, meta: { titleKey: 'menu.categories' } },
    { path: '/marcas', component: MarcasView, meta: { titleKey: 'menu.brands' } },
    {
      path: '/centros-distribucion',
      component: CentrosDistribucionView,
      meta: { titleKey: 'menu.distributionCenters' },
    },
    { path: '/tipos-cambio', component: TiposCambioView, meta: { titleKey: 'menu.exchangeRates' } },
    { path: '/productos', component: ProductosView, meta: { titleKey: 'menu.products' } },
    { path: '/inventario', component: InventarioView, meta: { titleKey: 'menu.inventory' } },
    { path: '/precios', component: PreciosView, meta: { titleKey: 'menu.prices' } },
    { path: '/descuentos', component: DescuentosView, meta: { titleKey: 'menu.discounts' } },
  ],
})
