<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Buscar...' },
})
defineEmits(['update:modelValue'])
</script>
<template>
  <div class="search-input">
    <i class="bi bi-search"></i
    ><input
      type="search"
      class="form-control"
      :value="modelValue"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>
<style scoped>
.search-input {
  position: relative;
}
.search-input i {
  position: absolute;
  top: 50%;
  left: 0.85rem;
  z-index: 2;
  color: #929baa;
  transform: translateY(-50%);
}
.search-input .form-control {
  padding-left: 2.4rem;
}
</style>
