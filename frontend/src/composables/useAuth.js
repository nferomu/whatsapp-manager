import { ref } from 'vue'
import { supabase } from '../services/supabase'

export const user = ref(null)
export const error = ref(null)

export async function login(email, password) {
  const { data, error: err } = await supabase.auth.signInWithPassword({ email, password })
  if (err) {
    error.value = err.message
    return false
  }
  user.value = data.user
  error.value = null
  localStorage.setItem('sb_user', JSON.stringify(user.value))
  return true
}

export function logout() {
  supabase.auth.signOut()
  user.value = null
  localStorage.removeItem('sb_user')
}

export function loadUser() {
  const saved = localStorage.getItem('sb_user')
  if (saved) user.value = JSON.parse(saved)
}
