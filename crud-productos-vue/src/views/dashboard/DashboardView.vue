<script setup>
import PageHeader from '@/components/common/PageHeader.vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const stats = computed(() => [
  {
    label: t('dashboard.products'),
    value: '1,245',
    icon: 'bi-box-seam',
    tone: 'blue',
    detail: t('dashboard.registeredCatalog'),
  },
  {
    label: t('dashboard.categories'),
    value: '32',
    icon: 'bi-tags',
    tone: 'green',
    detail: t('dashboard.activeCategories'),
  },
  {
    label: t('dashboard.centers'),
    value: '5',
    icon: 'bi-building',
    tone: 'purple',
    detail: t('dashboard.distributionCenters'),
  },
  {
    label: t('dashboard.lowStock'),
    value: '18',
    icon: 'bi-exclamation-triangle',
    tone: 'orange',
    detail: t('dashboard.requireAttention'),
  },
])
</script>
<template>
  <PageHeader
    :title="t('dashboard.title')"
    :description="t('dashboard.description')"
    :breadcrumbs="[t('common.breadcrumbs.home'), t('menu.dashboard')]"
  />
  <div class="row g-3 g-xl-4">
    <div v-for="stat in stats" :key="stat.label" class="col-sm-6 col-xl-3">
      <article class="card app-card h-100">
        <div class="card-body p-4">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <p class="text-secondary mb-2">{{ stat.label }}</p>
              <h3 class="mb-2">{{ stat.value }}</h3>
            </div>
            <span class="stat-icon" :class="stat.tone"><i class="bi" :class="stat.icon"></i></span>
          </div>
          <small class="text-secondary">{{ stat.detail }}</small>
        </div>
      </article>
    </div>
  </div>
  <div class="card app-card mt-4">
    <div class="card-body p-4 p-lg-5 text-center">
      <span class="welcome-icon"><i class="bi bi-clipboard-data"></i></span>
      <h4 class="mt-3">{{ t('dashboard.welcome') }}</h4>
      <p class="text-secondary mb-0">{{ t('dashboard.welcomeText') }}</p>
      <RouterLink to="/categorias" class="btn btn-primary mt-3"
        ><i class="bi bi-tags me-2"></i>{{ t('dashboard.manageCategories') }}</RouterLink
      >
    </div>
  </div>
</template>
<style scoped>
.card h3 {
  color: #202a3d;
  font-size: 1.9rem;
  font-weight: 750;
}
.card p {
  font-size: 0.86rem;
}
.stat-icon,
.welcome-icon {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 0.8rem;
  font-size: 1.25rem;
}
.blue {
  color: #3157d5;
  background: #e9edfc;
}
.green {
  color: #168260;
  background: #e8f7f1;
}
.purple {
  color: #7555c6;
  background: #f0ebfc;
}
.orange {
  color: #bf6a24;
  background: #fff1e4;
}
.welcome-icon {
  margin: auto;
  width: 58px;
  height: 58px;
  color: #3157d5;
  background: #e9edfc;
  font-size: 1.5rem;
}
</style>
