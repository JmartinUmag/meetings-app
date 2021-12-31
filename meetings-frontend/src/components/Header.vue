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
          <router-link :to="{ name: 'Home' }" class="navbar-item">
            <o-icon icon="home" size="small" class="mr-1"> </o-icon>
            Inicio
          </router-link>
          <router-link :to="{ name: 'ListUsers' }" class="navbar-item">
            <o-icon icon="account" size="small" class="mr-1"> </o-icon>
            Usuarios
          </router-link>
        </div>

        <div class="navbar-end">
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              {{ user }}
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

  const { user, clearToken } = useTokenStore()

  async function logout() {
    clearToken()
  }
</script>
