import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/main.css'

import { supabase } from './services/supabase'

const app = createApp(App)

supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    localStorage.setItem('user', JSON.stringify(session))
  } else if (event === 'SIGNED_OUT') {
    localStorage.removeItem('user')
  }
})

app.use(createPinia())
app.use(router)

app.mount('#app')
