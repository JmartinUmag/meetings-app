import { createApp } from 'vue'
import App from './App.vue'

import Oruga from '@oruga-ui/oruga-next'
// @ts-ignore
import { bulmaConfig } from 'oruga-ui/theme-bulma'
import { createPinia } from 'pinia'

import router from '@/router'

import '@oruga-ui/theme-bulma/dist/bulma.css'

createApp(App)
  .use(Oruga, bulmaConfig)
  .use(router)
  .use(createPinia())
  .mount('#app')
