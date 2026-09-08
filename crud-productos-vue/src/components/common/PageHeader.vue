<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  breadcrumbs: { type: Array, default: () => [] },
})
</script>
<template>
  <div class="page-header d-flex flex-wrap align-items-end justify-content-between gap-3 mb-4">
    <div>
      <nav v-if="breadcrumbs.length" aria-label="breadcrumb">
        <ol class="breadcrumb mb-2">
          <li
            v-for="(item, index) in breadcrumbs"
            :key="item"
            class="breadcrumb-item"
            :class="{ active: index === breadcrumbs.length - 1 }"
          >
            {{ item }}
          </li>
        </ol>
      </nav>
      <h2 class="mb-1">{{ title }}</h2>
      <p v-if="description" class="text-secondary mb-0">{{ description }}</p>
    </div>
    <div><slot name="actions" /></div>
  </div>
</template>
<style scoped>
.page-header h2 {
  color: #202a3d;
  font-size: 1.55rem;
  font-weight: 700;
}
.page-header p {
  font-size: 0.9rem;
}
.breadcrumb {
  font-size: 0.76rem;
}
.breadcrumb-item:not(.active) {
  color: #3157d5;
}
</style>
