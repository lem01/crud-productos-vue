<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
defineEmits(['toggle-sidebar'])
const route = useRoute()
const { t, locale } = useI18n()
const pageTitle = computed(() =>
  route.meta.titleKey ? t(route.meta.titleKey) : t('common.administration'),
)
function changeLanguage(code) {
  locale.value = code.toLowerCase()
  localStorage.setItem('app-locale', locale.value)
}
</script>
<template>
  <header class="app-navbar navbar bg-white sticky-top">
    <div class="container-fluid px-3 px-md-4">
      <button class="btn sidebar-toggle" aria-label="Abrir menú" @click="$emit('toggle-sidebar')">
        <i class="bi bi-list"></i>
      </button>
      <div class="ms-2">
        <small class="text-secondary d-none d-sm-block">{{ t('common.adminPanel') }}</small>
        <h1 class="navbar-title mb-0">{{ pageTitle }}</h1>
      </div>
      <div class="ms-auto d-flex align-items-center gap-2 gap-sm-3">
        <div class="language-switch d-flex">
          <button
            v-for="code in ['ES', 'EN']"
            :key="code"
            class="btn btn-sm"
            :class="{ active: locale === code.toLowerCase() }"
            @click="changeLanguage(code)"
          >
            {{ code }}
          </button>
        </div>
        <div class="user-area d-flex align-items-center gap-2">
          <span class="user-avatar">AD</span>
          <div class="d-none d-md-block lh-sm">
            <strong>Administrador</strong
            ><small class="d-block text-secondary">admin@sistema.com</small>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
<style scoped>
.app-navbar {
  min-height: 76px;
  border-bottom: 1px solid var(--app-border);
}
.sidebar-toggle {
  display: none;
  padding: 0.35rem 0.55rem;
  border-color: var(--app-border);
  font-size: 1.35rem;
}
.navbar-title {
  color: #202a3d;
  font-size: 1.15rem;
  font-weight: 650;
}
.app-navbar small {
  font-size: 0.72rem;
}
.language-switch {
  padding: 0.18rem;
  border: 1px solid var(--app-border);
  border-radius: 0.5rem;
  background: #f6f7f9;
}
.language-switch .btn {
  min-height: auto;
  padding: 0.18rem 0.48rem;
  border: 0;
  color: #7a8495;
  font-size: 0.7rem;
}
.language-switch .active {
  color: #233f9f;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}
.user-avatar {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  color: #3157d5;
  background: #e9edfc;
  font-size: 0.76rem;
  font-weight: 700;
}
.user-area strong {
  font-size: 0.82rem;
}
@media (max-width: 991.98px) {
  .sidebar-toggle {
    display: inline-flex;
  }
}
</style>
