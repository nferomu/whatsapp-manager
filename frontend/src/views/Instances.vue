<template>
  <div class="min-h-screen flex bg-gray-950 text-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
      <div class="p-6 text-center font-bold text-xl text-indigo-400 border-b border-gray-800">
        WhatsApp Manager
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <button
          @click="$router.push('/dashboard')"
          class="w-full text-left py-2.5 px-4 rounded-lg hover:bg-gray-800 transition flex items-center gap-2"
        >
          📊 Dashboard
        </button>
        <button
          class="w-full text-left py-2.5 px-4 rounded-lg bg-indigo-600 hover:bg-indigo-700 transition flex items-center gap-2"
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

    <!-- Main Content -->
    <main class="flex-1 p-8">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold">Gerenciamento de Instâncias</h1>
        <button
          @click="refreshStatus"
          :disabled="refreshing"
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 px-4 py-2 rounded-lg shadow-lg"
        >
          {{ refreshing ? 'Atualizando...' : 'Atualizar Status' }}
        </button>
      </div>

      <!-- Botão abrir modal -->
      <button
        @click="openModal = true"
        class="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg shadow-lg mb-6"
      >
        Criar Nova Instância
      </button>

      <!-- Modal de criação -->
      <div v-if="openModal" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-6 rounded-lg w-full max-w-md relative">
          <button @click="openModal = false" class="absolute top-3 right-3 text-gray-400 hover:text-gray-200">✖</button>
          <h2 class="text-xl font-bold mb-4">Nova Instância</h2>

          <div class="flex flex-col gap-3">
              <input v-model="newInstance" type="text" placeholder="Nome da instância" class="p-2 bg-gray-800 border border-gray-700 rounded" />
              
              <input
                  v-model="newPhoneNumber"
                  type="text"
                  placeholder="Número do WhatsApp (5599999999999)"
                  class="p-2 bg-gray-800 border border-gray-700 rounded"
              />

              <select v-model="newIntegration" class="p-2 bg-gray-800 border border-gray-700 rounded">
                  <option value="WHATSAPP-BAILEYS">WHATSAPP-BAILEYS</option>
                  <option value="WHATSAPP-BUSINESS">WHATSAPP-BUSINESS</option>
                  <option value="EVOLUTION">EVOLUTION</option>
              </select>
          </div>

          <button
            @click="createInstance"
            :disabled="loading"
            class="bg-green-600 hover:bg-green-700 disabled:bg-green-400 px-4 py-2 mt-4 rounded text-white w-full flex items-center justify-center gap-2"
          >
            <div v-if="loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            {{ loading ? 'Criando...' : 'Criar Instância' }}
          </button>
        </div>
      </div>

      <!-- Modal QR Code -->
      <div v-if="showQRModal" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-6 rounded-lg w-full max-w-md relative">
          <button @click="showQRModal = false" class="absolute top-3 right-3 text-gray-400 hover:text-gray-200">✖</button>
          <h2 class="text-xl font-bold mb-4">QR Code - {{ selectedInstance?.name }}</h2>
          
          <div class="flex justify-center mb-4">
            <img :src="selectedInstance?.qrcode" alt="QR Code" class="w-64 h-64 border border-gray-700 rounded" />
          </div>
          
          <p class="text-gray-400 text-sm text-center">
            Escaneie este QR Code com seu WhatsApp para conectar a instância
          </p>
        </div>
      </div>

      <!-- Modal de Confirmação -->
      <div v-if="showConfirmModal" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-6 rounded-lg w-full max-w-md relative">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-yellow-600 rounded-full flex items-center justify-center">
              <span class="text-white text-xl">⚠</span>
            </div>
            <h2 class="text-xl font-bold">Confirmar Exclusão</h2>
          </div>
          
          <p class="text-gray-300 mb-6">
            Tem certeza que deseja excluir a instância <strong>{{ instanceToDelete?.name }}</strong>?
            Esta ação não pode ser desfeita.
          </p>
          
          <div class="flex gap-3">
            <button
              @click="showConfirmModal = false"
              class="flex-1 py-2 px-4 bg-gray-600 hover:bg-gray-700 rounded text-white"
            >
              Cancelar
            </button>
            <button
              @click="confirmDelete"
              :disabled="deleting"
              class="flex-1 py-2 px-4 bg-red-600 hover:bg-red-700 disabled:bg-red-400 rounded text-white flex items-center justify-center gap-2"
            >
              <div v-if="deleting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              {{ deleting ? 'Excluindo...' : 'Excluir' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de Sucesso -->
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-6 rounded-lg w-full max-w-md relative">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center">
              <span class="text-white text-xl">✓</span>
            </div>
            <h2 class="text-xl font-bold text-green-400">Sucesso!</h2>
          </div>
          
          <p class="text-gray-300 mb-6">{{ successMessage }}</p>
          
          <button
            @click="showSuccessModal = false"
            class="w-full py-2 px-4 bg-green-600 hover:bg-green-700 rounded text-white"
          >
            OK
          </button>
        </div>
      </div>

      <!-- Modal de Erro -->
      <div v-if="showErrorModal" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-6 rounded-lg w-full max-w-md relative">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center">
              <span class="text-white text-xl">✗</span>
            </div>
            <h2 class="text-xl font-bold text-red-400">Erro!</h2>
          </div>
          
          <p class="text-gray-300 mb-6">{{ errorMessage }}</p>
          
          <button
            @click="showErrorModal = false"
            class="w-full py-2 px-4 bg-red-600 hover:bg-red-700 rounded text-white"
          >
            OK
          </button>
        </div>
      </div>

      <!-- Lista de instâncias -->
      <div v-if="instances.length === 0" class="text-gray-400 text-center py-8">
        <div class="text-6xl mb-4">📱</div>
        <p>Nenhuma instância registrada.</p>
        <p class="text-sm">Clique em "Criar Nova Instância" para começar.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="instance in instances" :key="instance.id" class="p-6 bg-gray-900 rounded-lg border border-gray-700 shadow-lg hover:shadow-xl transition-shadow">
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <h3 class="font-semibold text-lg text-white mb-1">{{ instance.name }}</h3>
              <p class="text-gray-400 text-sm mb-2">{{ instance.phone_number }}</p>
              <div class="flex items-center gap-2">
                <span class="text-gray-500 text-sm">Status:</span>
                <span :class="statusColor(instance.status)" class="font-medium">
                  {{ getStatusText(instance.status) }}
                </span>
              </div>
            </div>
            <div class="flex gap-2">
              <button 
                @click="showQR(instance)" 
                class="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-white text-sm"
                title="Ver QR Code"
              >
                QR
              </button>
              <button 
                @click="deleteInstance(instance.instance_id)" 
                class="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-white text-sm"
                title="Excluir Instância"
              >
                ✖
              </button>
            </div>
          </div>

          <div class="text-gray-500 text-xs break-all mb-3">
            <span class="font-medium">ID:</span> {{ instance.instance_id }}
          </div>

          <div class="text-gray-500 text-xs">
            <span class="font-medium">Integração:</span> {{ instance.integration }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";
import { supabase } from "@/services/supabase";

const instances = ref([]);
const openModal = ref(false);
const showQRModal = ref(false);
const showConfirmModal = ref(false);
const showSuccessModal = ref(false);
const showErrorModal = ref(false);
const selectedInstance = ref(null);
const instanceToDelete = ref(null);
const successMessage = ref("");
const errorMessage = ref("");
const newInstance = ref("");
const newPhoneNumber = ref("");
const newIntegration = ref("WHATSAPP-BAILEYS");
const loading = ref(false);
const refreshing = ref(false);
const deleting = ref(false);

const logout = async () => {
  await supabase.auth.signOut();
  window.location.href = "/login";
};

const statusColor = (status) => {
  if (status === "open" || status === "connected") return "text-green-400";
  if (status === "connecting" || status === "disconnected") return "text-yellow-400";
  if (status === "error" || status === "closed") return "text-red-400";
  return "text-gray-400";
};

const getStatusText = (status) => {
  const statusMap = {
    "open": "Conectado",
    "connected": "Conectado", 
    "connecting": "Conectando",
    "disconnected": "Desconectado",
    "error": "Erro",
    "closed": "Fechado"
  };
  return statusMap[status] || status;
};

const loadInstances = async () => {
  try {
    const res = await api.get("/instances");
    instances.value = res.data.map((inst) => ({
      ...inst,
      qrcode: inst.qrcode || `data:image/png;base64,${inst.qrcode}`,
    }));
  } catch (error) {
    console.error("Erro ao carregar instâncias:", error);
    instances.value = [];
  }
};

const createInstance = async () => {
  if (!newInstance.value || !newPhoneNumber.value) {
    errorMessage.value = "Preencha todos os campos obrigatórios.";
    showErrorModal.value = true;
    return;
  }

  try {
    loading.value = true;
    await api.post("/instances/create", {
      name: newInstance.value,
      phone_number: newPhoneNumber.value,
      integration: newIntegration.value
    });
    
    openModal.value = false;
    newInstance.value = "";
    newPhoneNumber.value = "";
    newIntegration.value = "WHATSAPP-BAILEYS";
    await loadInstances();
    
    successMessage.value = "Instância criada com sucesso!";
    showSuccessModal.value = true;
  } catch (err) {
    console.error(err);
    errorMessage.value = "Erro ao criar instância: " + (err.response?.data?.detail || err.message);
    showErrorModal.value = true;
  } finally {
    loading.value = false;
  }
};

const deleteInstance = async (instance_id) => {
  const instance = instances.value.find(inst => inst.instance_id === instance_id);
  instanceToDelete.value = instance;
  showConfirmModal.value = true;
};

const confirmDelete = async () => {
  try {
    deleting.value = true;
    await api.delete(`/instances/${instanceToDelete.value.instance_id}`);
    await loadInstances();
    showConfirmModal.value = false;
    successMessage.value = "Instância excluída com sucesso!";
    showSuccessModal.value = true;
  } catch (error) {
    console.error("Erro ao excluir instância:", error);
    errorMessage.value = "Erro ao excluir instância: " + (error.response?.data?.detail || error.message);
    showErrorModal.value = true;
  } finally {
    deleting.value = false;
  }
};

const showQR = (instance) => {
  selectedInstance.value = instance;
  showQRModal.value = true;
};

const refreshStatus = async () => {
  try {
    refreshing.value = true;
    await api.post("/instances/refresh-status");
    await loadInstances();
    successMessage.value = "Status das instâncias atualizado com sucesso!";
    showSuccessModal.value = true;
  } catch (error) {
    console.error("Erro ao atualizar status:", error);
    errorMessage.value = "Erro ao atualizar status: " + (error.response?.data?.detail || error.message);
    showErrorModal.value = true;
  } finally {
    refreshing.value = false;
  }
};

// Atualização automática do status a cada 30 segundos
const startAutoRefresh = () => {
  setInterval(async () => {
    try {
      await api.post("/instances/refresh-status");
      await loadInstances();
    } catch (error) {
      console.error("Erro na atualização automática:", error);
    }
  }, 30000);
};

onMounted(() => {
  loadInstances();
  startAutoRefresh();
});
</script>
