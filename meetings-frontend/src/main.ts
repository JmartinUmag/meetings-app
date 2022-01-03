import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Oruga from '@oruga-ui/oruga-next'
// @ts-ignore
import { bulmaConfig } from '@oruga-ui/theme-bulma'
import '@oruga-ui/theme-bulma/dist/bulma.css'

import '@/assets/styles.scss'

import App from '@/App.vue'
import router from '@/router'

const orugaConfig = {
  ...bulmaConfig,
  iconPack: 'mdi',
}

createApp(App)
  .use(Oruga, orugaConfig)
  .use(router)
  .use(createPinia())
  .mount('#app')
