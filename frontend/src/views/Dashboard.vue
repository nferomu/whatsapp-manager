<template>
  <div class="min-h-screen flex bg-gray-950 text-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
      <div class="p-6 text-center font-bold text-xl text-indigo-400 border-b border-gray-800">
        WhatsApp Manager
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <button
          class="w-full text-left py-2.5 px-4 rounded-lg hover:bg-gray-800 transition flex items-center gap-2"
        >
          📊 Dashboard
        </button>
        <button
          @click="$router.push('/instances')"
          class="w-full text-left py-2.5 px-4 rounded-lg hover:bg-gray-800 transition flex items-center gap-2"
        >
          💬 Instâncias
        </button>
      </nav>

      <div class="p-4 border-t border-gray-800">
        <button
          @click="logout"
          class="w-full py-2 rounded-lg bg-red-600 hover:bg-red-700 transition text-white font-semibold"
        >
          Sair
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 p-10">
      <h1 class="text-3xl font-bold mb-8">Visão Geral</h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-gray-900 rounded-xl border border-gray-800 shadow hover:shadow-lg transition">
          <p class="text-gray-400">Total de Instâncias</p>
          <h2 class="text-4xl font-bold mt-2 text-indigo-400">8</h2>
        </div>
        <div class="p-6 bg-gray-900 rounded-xl border border-gray-800 shadow hover:shadow-lg transition">
          <p class="text-gray-400">Mensagens Enviadas</p>
          <h2 class="text-4xl font-bold mt-2 text-green-400">342</h2>
        </div>
        <div class="p-6 bg-gray-900 rounded-xl border border-gray-800 shadow hover:shadow-lg transition">
          <p class="text-gray-400">Mensagens Recebidas</p>
          <h2 class="text-4xl font-bold mt-2 text-blue-400">289</h2>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { supabase } from "@/services/supabase";

const logout = async () => {
  await supabase.auth.signOut();
  window.location.href = "/login";
};
</script>
