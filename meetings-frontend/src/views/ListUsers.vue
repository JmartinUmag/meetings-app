<template>
  <div class="container mt-4">
    <h1 class="page-title">Usuarios</h1>

    <div class="level-right">
      <div class="buttons">
        <o-button variant="primary" icon-left="plus"> Nuevo</o-button>
        <o-button
          variant="primary"
          icon-left="reload"
          :disabled="loading"
          @click="loadUsers"
        >
          Recargar
        </o-button>
      </div>
    </div>

    <o-table :data="users" :loading="loading">
      <o-table-column field="username" label="Usuario" v-slot="props">
        {{ props.row.username }}
      </o-table-column>
      <o-table-column field="fullname" label="Nombre" v-slot="props">
        {{ props.row.fullname }}
      </o-table-column>
      <o-table-column field="roles" label="Roles" v-slot="props">
        <span
          v-for="role in props.row.roles"
          :key="role.id"
          class="tag is-info is-light"
        >
          {{ role.name }}
        </span>
      </o-table-column>
    </o-table>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { User } from '@/interfaces'
  import { getUsers } from '@/api'

  const users = ref<User[]>([])
  const loading = ref(false)

  async function loadUsers() {
    loading.value = true
    users.value = await getUsers()
    loading.value = false
  }

  loadUsers()
</script>
