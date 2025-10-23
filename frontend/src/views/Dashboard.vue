

<template>
  <AppLayout>
    <div class="p-6">
        <h1 class="text-2xl font-bold mb-4">Dashboard Geral</h1>
        <div class="grid grid-cols-2 gap-4">
        <div class="p-4 bg-white shadow rounded">
            <p>Total de números cadastrados: 0</p>
        </div>
        <div class="p-4 bg-white shadow rounded">
            <p>Total de mensagens enviadas: 0</p>
        </div>
        </div>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'
</script>
