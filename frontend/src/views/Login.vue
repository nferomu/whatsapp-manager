<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <div class="w-full max-w-md bg-gray-900/70 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-gray-700">
      <h2 class="text-3xl font-bold text-center text-white mb-6">🚀 WhatsApp Manager</h2>
      <p class="text-gray-400 text-center mb-8">Entre com suas credenciais do sistema</p>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="block text-gray-300 mb-2">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="exemplo@email.com"
            class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-300 mb-2">Senha</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition duration-200"
        >
          Entrar
        </button>
      </form>

      <p v-if="errorMessage" class="text-red-500 text-center mt-4">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { supabase } from "@/services/supabase";

const email = ref("");
const password = ref("");
const errorMessage = ref("");

const handleLogin = async () => {
  const { error } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  });
  if (error) {
    errorMessage.value = "Credenciais inválidas. Verifique e tente novamente.";
  } else {
    window.location.href = "/dashboard";
  }
};
</script>
