<template>
  <Header v-if="isAuthenticated" />

  <router-view />
</template>

<script setup lang="ts">
  import Header from '@/components/Header.vue'
  import { useTokenStore } from '@/stores/token'
  import { storeToRefs } from 'pinia'

  let { isAuthenticated } = storeToRefs(useTokenStore())
</script>
