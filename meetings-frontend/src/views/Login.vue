<template>
  <section class="hero is-dark is-fullheight">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-5-tablet is-4-desktop is-3-widescreen">
            <form class="box">
              <h2 class="subtitle has-text-dark has-text-centered my-0">
                {{ appName }}
              </h2>
              <hr class="my-4" />
              <div class="field">
                <p class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    placeholder="Usuario"
                    v-model="username"
                    required
                  />
                  <span class="icon is-small is-left">
                    <o-icon icon="account" />
                  </span>
                </p>
              </div>
              <div class="field has-addons">
                <p class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    :type="passwordFieldType"
                    placeholder="Contraseña"
                    v-model="password"
                    required
                  />
                  <span class="icon is-small is-left">
                    <o-icon icon="form-textbox-password" />
                  </span>
                  <span class="icon is-medium is-right">
                    <o-icon
                      :icon="passwordIcon"
                      clickable
                      @click="showPassword = !showPassword"
                    />
                  </span>
                </p>
              </div>
              <div
                v-if="errorMessage !== ''"
                class="message is-small is-danger my-0"
              >
                <div class="message-body py-2">{{ errorMessage }}</div>
              </div>
              <o-field class="mt-4">
                <o-button
                  variant="success"
                  expanded
                  :disabled="loading"
                  @click="login"
                >
                  <o-loading
                    :active="loading"
                    :full-page="false"
                    overlay-class=""
                  />
                  <span v-if="!loading">Iniciar Sesión</span>
                </o-button>
              </o-field>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useTokenStore } from '@/stores/token'
  import { getMyUser, login as apiLogin } from '@/api'
  import { isApiError } from '@/utilities'

  const { setToken, setUser } = useTokenStore()
  const router = useRouter()
  const appName = import.meta.env.VITE_APP_NAME

  const username = ref('')
  const password = ref('')
  const showPassword = ref(false)
  const errorMessage = ref('')
  const loading = ref(false)

  const passwordFieldType = computed(() =>
    showPassword.value ? 'text' : 'password'
  )
  const passwordIcon = computed(() => (showPassword.value ? 'eye' : 'eye-off'))

  async function login() {
    loading.value = true
    errorMessage.value = ''
    try {
      // set token
      const tokenData = await apiLogin(username.value, password.value)
      setToken(tokenData.accessToken, tokenData.tokenType)

      // set user
      const user = await getMyUser()
      setUser(user)

      await router.push({ name: 'Home' })
    } catch (error) {
      if (isApiError(error) && error.status === 401) {
        errorMessage.value = 'Usuario y/o contraseña incorrectos'
      } else {
        console.error(error)
      }
    } finally {
      loading.value = false
    }
  }
</script>
