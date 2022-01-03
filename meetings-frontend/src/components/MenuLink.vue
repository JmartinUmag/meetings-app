<template>
  <router-link v-show="allowed" :to="{ name: routeName }" class="navbar-item">
    <o-icon v-if="icon" :icon="icon" size="small" class="mr-1"> </o-icon>
    {{ label }}
  </router-link>
</template>

<script setup lang="ts">
  import { computed } from 'vue'
  import { checkRoutePermission } from '@/utilities'

  const props = defineProps<{
    routeName: string
    label: string
    icon?: string
  }>()

  const allowed = computed(() => checkRoutePermission(props.routeName))
</script>

<style scoped></style>
