<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 backdrop-blur-md bg-gray-800/50">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-3xl p-4 md:p-6 max-h-[90vh] overflow-auto">
      <div v-if="!selectedExercise" class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold text-gray-800">Виберіть вправу</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700" aria-label="Close">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div v-if="!selectedExercise" class="mb-4 w-full">
        <div class="relative">
          <input
            type="text"
            placeholder="Пошук вправи"
            v-model="searchQuery"
            @input="onSearch(searchQuery)"
            class="w-full px-4 py-3 text-lg text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            aria-label="Пошук вправи"
          />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-center my-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg my-4">
        {{ error }}
      </div>
      <div v-else-if="selectedExercise" class="mb-4">
        <h3 class="text-xl font-medium text-gray-800 mb-3">Дані вправи:</h3>
        <div class="h-px bg-gray-200 w-full mb-4"></div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">Назва</h4>
            <p class="text-gray-800 font-bold text-lg">{{ selectedExercise.name }}</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">Тип</h4>
            <p class="text-gray-800 font-bold">{{ formatExerciseType(selectedExercise.type) }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-1 gap-4 mb-6">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">Опис</h4>
            <p class="text-gray-800">{{ selectedExercise.description || 'Немає опису' }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Рекомендована тривалість</h4>
            <div class="mb-4">
              <p class="text-gray-800 font-bold">{{ selectedExercise.duration }} хв / {{ selectedExercise.calories_burned }} ккал</p>
            </div>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Інтенсивність</h4>
            <p class="text-gray-800 font-bold">{{ formatIntensity(selectedExercise.intensity) }}</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Калорії</h4>
            <p class="text-gray-800 font-bold">{{ selectedExercise.calories_burned }} ккал</p>
          </div>
        </div>

        <div class="flex items-center gap-4 mt-6">
          <div class="flex-1">
            <label for="duration" class="block text-sm font-medium text-gray-700 mb-1">Тривалість (хв):</label>
            <input 
              id="duration" 
              v-model.number="duration" 
              type="number" 
              min="1" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" 
              placeholder="Тривалість у хвилинах"
            />
          </div>
          <div class="flex-1">
            <h4 class="block text-sm font-medium text-gray-700 mb-1">Розраховані калорії:</h4>
            <div class="text-gray-800 py-2">
              {{ calculatedCalories }} ккал за {{ duration }} хв
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-4 mt-4">
          <button 
            @click="$emit('close')"
            class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-medium transition-colors"
          >
            Скасувати
          </button>
          <button 
            @click="addExercise"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors"
            :disabled="!duration || duration <= 0"
          >
            Додати
          </button>
        </div>
      </div>

      <div v-else-if="searchResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(exercise, index) in searchResults" 
          :key="index"
          @click="selectExercise(exercise)"
          class="p-4 border border-gray-200 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors"
        >
          <div class="flex items-center">
            <div>
              <h4 class="font-medium text-gray-800">{{ exercise.name }}</h4>
              <p class="text-sm text-gray-500">{{ exercise.duration }} хв / {{ exercise.calories_burned }} ккал</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="p-4 text-center text-gray-500">
        <p>Почніть пошук щоб побачити результати</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ExerciseSelectionModal',
  components: {},
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedExercise: null,
      duration: null,
      isLoading: false,
      error: null
    };
  },
  computed: {
    calculatedCalories() {
      if (!this.selectedExercise || !this.duration) return 0;
      const ratio = this.duration / this.selectedExercise.duration;
      return Math.round(this.selectedExercise.calories_burned * ratio);
    }
  },
  mounted() {
    this.fetchExercises();
    document.addEventListener('keydown', this.handleEscape);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscape);
  },
  methods: {
    async fetchExercises() {
      try {
        this.isLoading = true;
        this.error = null;
        const response = await axios.get('/api/exercises/exercises/', {
          params: { search: this.searchQuery }
        });
        this.searchResults = response.data;
      }
      catch (error) {
        console.error('Error fetching exercises:', error);
        this.error = 'Не вдалося завантажити вправи';
      }
      finally {
        this.isLoading = false;
      }
    },
    onSearch(query) {
      this.searchQuery = query;
      this.fetchExercises();
    },
    async selectExercise(exercise) {
      this.selectedExercise = null;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/exercises/exercises/${exercise.id}/`);
        const detail = response.data;
        this.selectedExercise = {
          id: detail.id,
          name: detail.name,
          type: detail.type,
          description: detail.description,
          intensity: detail.intensity,
          duration: detail.duration,
          calories_burned: detail.calories_burned
        };
        this.duration = detail.duration;
      }
      catch (e) {
        console.error('Error fetching exercise details:', e);
        this.error = 'Не вдалося завантажити деталі вправи';
      }
      finally {
        this.isLoading = false;
      }
    },
    addExercise() {
      if (this.selectedExercise && this.duration > 0) {
        const exerciseData = {
          id: this.selectedExercise.id,
          exercise: this.selectedExercise.id,
          name: this.selectedExercise.name,
          type: this.selectedExercise.type,
          description: this.selectedExercise.description,
          intensity: this.selectedExercise.intensity,
          duration: this.duration,
          date: new Date().toISOString().split('T')[0],
          calories_burned: this.calculatedCalories
        };
        this.$emit('add-exercise', exerciseData);
      }
    },
    formatExerciseType(type) {
      const typeMap = {
        'аеробна': 'Аеробна',
        'силова': 'Силова',
        'розтяжка': 'Розтяжка',
      };
      return typeMap[type] || type;
    },
    formatIntensity(intensity) {
      const intensityMap = {
        'низька': 'Низька',
        'середня': 'Середня',
        'висока': 'Висока'
      };
      return intensityMap[intensity] || intensity;
    },
    handleEscape(e) {
      if (e.key === 'Escape') {
        this.$emit('close');
      }
    }
  }
};
</script> 
