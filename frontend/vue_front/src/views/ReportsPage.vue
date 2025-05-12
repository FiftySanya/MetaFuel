<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <div class="container mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Звіт за планом</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Оберіть план</label>
            <select v-model="selectedPlan" class="w-full border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500">
              <option disabled value="">-- Виберіть план --</option>
              <option v-for="plan in plans" :key="plan.id" :value="plan.id">
                {{ plan.id }}: {{ plan.start_date }} – {{ plan.end_date }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Тип графіку</label>
            <select v-model="chartType" class="w-full border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500">
              <option disabled value="">-- Виберіть тип --</option>
              <option value="weight">Прогрес ваги</option>
              <option value="consumed">Споживання калорій</option>
              <option value="burned">Витрата калорій</option>
            </select>
          </div>
          <div class="flex items-end">
            <button 
              @click="loadReport" 
              :disabled="!selectedPlan || !chartType || isLoading"
              class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              Завантажити
            </button>
          </div>
        </div>
        <div v-if="isLoading" class="text-center py-6">
          <div class="animate-spin h-8 w-8 border-4 border-blue-600 border-b-transparent rounded-full mx-auto"></div>
        </div>
        <ProgressCharts
          v-else-if="loaded && selectedPlan && chartType"
          :plan-id="selectedPlan"
          :chart-type="chartType"
          :active-key="chartKey"
          :key="chartKey"
        />
        <div v-else class="text-center text-gray-500 py-6">Оберіть план та тип графіку, щоб побачити звіт</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import AppHeader from '@/components/AppHeader.vue';
import ProgressCharts from '@/components/ProgressCharts.vue';

export default {
  name: 'ReportsPage',
  components: { AppHeader, ProgressCharts },
  setup() {
    const router = useRouter();
    const plans = ref([]);
    const selectedPlan = ref('');
    const chartType = ref('');
    const isLoading = ref(false);
    const loaded = ref(false);
    const chartKey = ref(0);

    onMounted(async () => {
      try {
        const res = await axios.get('/api/plans/plans/');
        plans.value = res.data;
        if (plans.value.length > 0) {
          const lastPlan = plans.value[plans.value.length - 1];
          selectedPlan.value = lastPlan.id;
        }
      }
      catch (e) {
        console.error('Error loading plans:', e);
      }
    });

    const loadReport = () => {
      if (!selectedPlan.value || !chartType.value) return;
      isLoading.value = true;
      loaded.value = false;
      chartKey.value += 1;
      isLoading.value = false;
      loaded.value = true;
    };

    return {
      plans,
      selectedPlan,
      chartType,
      isLoading,
      loaded,
      chartKey,
      loadReport
    };
  }
};
</script> 
