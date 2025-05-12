<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <div class="container mx-auto px-4 py-8">
      <DateSelector @date-changed="updateDate" />
      
      <div class="mb-10">
        <section class="mb-6 bg-white rounded-lg shadow-md overflow-hidden">
          <div class="flex justify-between items-center p-4 bg-blue-50">
            <h2 class="text-xl font-semibold text-gray-800">Вправи</h2>
            <button
              @click="showExerciseModal = true"
              class="px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg transition-colors font-medium"
            >
              Додати
            </button>
          </div>

          <div v-if="isLoading" class="flex justify-center my-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>

          <div v-else-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg m-4">
            {{ error }}
          </div>

          <div v-else-if="exerciseItems.length === 0" class="p-6 text-center text-gray-500">
            Немає доданих вправ
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full bg-white">
              <thead class="bg-gray-50 border-b border-gray-200 text-gray-700">
                <tr>
                  <th class="p-4 font-medium text-left">Назва</th>
                  <th class="p-4 font-medium text-left">Тип</th>
                  <th class="p-4 font-medium text-left">Хвилини</th>
                  <th class="p-4 font-medium text-left">Калорії</th>
                  <th class="p-4 font-medium text-center">Дії</th>
                </tr>
              </thead>
              <transition-group name="fade" tag="tbody" class="bg-white divide-y divide-gray-200">
                <tr 
                  v-for="(exercise, index) in exerciseItems" 
                  :key="exercise.id" 
                >
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="text-gray-800">{{ exercise.name }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="text-gray-600">{{ formatExerciseType(exercise.type) }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="text-gray-600">{{ exercise.duration }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="text-gray-600">{{ exercise.caloriesBurned }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap text-center">
                    <button @click="removeExercise(index)" class="text-red-500 hover:text-red-700" aria-label="Remove item">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </transition-group>
            </table>
          </div>
        </section>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Загальна активність</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="text-lg font-medium text-gray-700 mb-2">Загальний час</h3>
            <p class="text-2xl font-bold text-blue-800">{{ totalDuration }} хв</p>
          </div>
          <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="text-lg font-medium text-gray-700 mb-2">Спалено калорій</h3>
            <p class="text-2xl font-bold text-blue-800">{{ totalCaloriesBurned }} ккал</p>
          </div>
        </div>
      </div>

      <ExerciseSelectionModal 
        v-if="showExerciseModal"
        @close="showExerciseModal = false"
        @add-exercise="addExercise"
      />
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import DateSelector from '@/components/DateSelector.vue';
import ExerciseSelectionModal from '@/components/ExerciseSelectionModal.vue';
import axios from 'axios';

export default {
  name: 'ExercisePage',
  components: {
    AppHeader,
    DateSelector,
    ExerciseSelectionModal
  },
  data() {
    return {
      selectedDate: new Date(),
      exerciseItems: [],
      showExerciseModal: false,
      isLoading: false,
      error: null
    };
  },
  computed: {
    formattedDate() {
      const date = this.selectedDate;
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    },
    totalDuration() {
      return this.exerciseItems.reduce((sum, item) => sum + parseInt(item.duration || 0), 0);
    },
    totalCaloriesBurned() {
      return this.exerciseItems.reduce((sum, item) => sum + parseInt(item.caloriesBurned || 0), 0);
    }
  },
  created() {
    this.fetchExercises();
  },
  methods: {
    async updateDate(date) {
      this.selectedDate = date;
      await this.fetchExercises();
    },
    async fetchExercises() {
      try {
        this.isLoading = true;
        this.error = null;
        const response = await axios.get('/api/exercises/exercise-items/', {
          params: { date: this.formattedDate }
        });
        
        this.exerciseItems = [];
        
        if (response.data && response.data.length > 0) {
          response.data.forEach(exercise => {
            const exerciseDetails = exercise.exercise_details || {};
            this.exerciseItems.push({
              id: exercise.id,
              name: exerciseDetails.name,
              type: exerciseDetails.type,
              duration: exercise.duration,
              caloriesBurned: exercise.calories_burned
            });
          });
        }
      }
      catch (error) {
        console.error('Error fetching exercises:', error);
        this.error = 'Не вдалося завантажити дані про вправи';
      }
      finally {
        this.isLoading = false;
      }
    },
    async addExercise(exerciseData) {
      try {
        this.isLoading = true;
        this.error = null;
        
        const data = {
          exercise: exerciseData.exercise,
          duration: exerciseData.duration,
          date: this.formattedDate
        };
        
        await axios.post('/api/exercises/exercise-items/', data);
        
        await this.fetchExercises();
        
        this.showExerciseModal = false;
      }
      catch (error) {
        console.error('Error adding exercise:', error);
        this.error = 'Не вдалося додати вправу';
      }
      finally {
        this.isLoading = false;
      }
    },
    async removeExercise(index) {
      try {
        this.isLoading = true;
        this.error = null;
        const item = this.exerciseItems[index];
        
        if (item && item.id) {
          await axios.delete(`/api/exercises/exercise-items/${item.id}/`);
          
          await this.fetchExercises();
        }
      }
      catch (error) {
        console.error('Error removing exercise:', error);
        this.error = 'Не вдалося видалити вправу';
      } 
      finally {
        this.isLoading = false;
      }
    },
    formatExerciseType(type) {
      const typeMap = {
        'аеробна': 'Аеробна',
        'силова': 'Силова',
        'розтяжка': 'Розтяжка',
      };
      return typeMap[type] || type || "Не вказано";
    }
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style> 
