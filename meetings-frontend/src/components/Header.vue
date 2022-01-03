<template>
  <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
    <div class="container">
      <div class="navbar-brand">
        <a
          role="button"
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbarBasicExample"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <MenuLink route-name="Home" label="Inicio" icon="home" />
          <MenuLink route-name="ListUsers" label="Usuarios" icon="account" />
        </div>

        <div class="navbar-end">
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              {{ user?.fullname }}
            </a>

            <div class="navbar-dropdown">
              <a class="navbar-item" @click="logout">Cerrar Sesión</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
  import { useTokenStore } from '@/stores/token'
  import { useRouter } from 'vue-router'
  import { User } from '@/interfaces'
  import MenuLink from '@/components/MenuLink.vue'

  const router = useRouter()
  const tokenStore = useTokenStore()
  const user: User | null = tokenStore.user

  async function logout() {
    tokenStore.clearData()
    await router.push({ name: 'Login' })
  }
</script>
