<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 backdrop-blur-md bg-gray-800/50">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-3xl p-4 md:p-6 max-h-[90vh] overflow-auto">
      <div v-if="!selectedFood" class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold text-gray-800">Оберіть страву або продукт</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700" aria-label="Close">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div v-if="!selectedFood" class="mb-4 w-full">
        <div class="relative">
          <input
            type="text"
            placeholder="Пошук страви або продукту"
            v-model="searchQuery"
            @input="onSearch(searchQuery)"
            class="w-full px-4 py-3 text-lg text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            aria-label="Пошук страви або продукту"
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
      <div v-else-if="selectedFood" class="mb-4">
        <h3 class="text-xl font-medium text-gray-800 mb-3">Дані продукту:</h3>
        <div class="h-px bg-gray-200 w-full mb-4"></div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">Основна інформація</h4>
            <p class="text-gray-800 font-bold text-lg">{{ selectedFood.name }}</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">Алергени</h4>
            <p class="text-gray-800">{{ selectedFood.allergens || 'Немає даних' }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Калорії</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.calories }} ккал</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Білки</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.proteins }} г</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Жири</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.fats }} г</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Вуглеводи</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.carbs }} г</p>
          </div>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Клітковина</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.fiber || 0 }} г</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Цукор</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.sugar || 0 }} г</p>
          </div>
          
          <div class="p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700">Натрій</h4>
            <p class="text-gray-800 font-bold">{{ selectedFood.nutrition.sodium || 0 }} мг</p>
          </div>
        </div>

        <div class="flex items-center gap-4 mt-6">
          <div class="flex-1">
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-1">Кількість (г):</label>
            <input 
              id="amount" 
              v-model.number="amount" 
              type="number" 
              min="1" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" 
              placeholder="Вага в грамах"
            />
          </div>
          <div class="flex-1">
            <h4 class="block text-sm font-medium text-gray-700 mb-1">Розраховані дані:</h4>
            <div class="text-gray-800 py-2">
              {{ calculatedCalories }} ккал / {{ amount }}г
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
            @click="addToMeal"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors"
            :disabled="!amount || amount <= 0"
          >
            Додати
          </button>
        </div>
      </div>

      <div v-else-if="searchResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(food, index) in searchResults" 
          :key="index"
          @click="selectFood(food)"
          class="p-4 border border-gray-200 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors"
        >
          <div class="flex items-center">
            <div>
              <h4 class="font-medium text-gray-800">{{ food.name }}</h4>
              <p class="text-sm text-gray-500">{{ food.nutrition.calories }} ккал / 100г</p>
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
  name: 'FoodSelectionModal',
  components: {},
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedFood: null,
      amount: 100,
      isLoading: false,
      error: null
    };
  },
  computed: {
    calculatedCalories() {
      if (!this.selectedFood || !this.amount) return 0;
      return ((this.selectedFood.nutrition.calories * this.amount) / 100).toFixed(1);
    }
  },
  mounted() {
    this.fetchProducts();
    document.addEventListener('keydown', this.handleEscape);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscape);
  },
  methods: {
    async fetchProducts() {
      try {
        this.isLoading = true;
        this.error = null;
        const response = await axios.get('/api/foods/products/', {
          params: { search: this.searchQuery }
        });
        const products = response.data;
        
        this.searchResults = products.map(product => ({
          id: product.id,
          name: product.name,
          allergens: product.allergens,
          nutrition: {
            calories: product.calories,
            proteins: product.protein,
            fats: product.fat,
            carbs: product.carbs,
            fiber: product.fiber,
            sugar: product.sugar,
            sodium: product.sodium
          }
        }));
      }
      catch (error) {
        console.error('Error fetching products:', error);
        this.error = 'Не вдалося завантажити продукти';
      }
      finally {
        this.isLoading = false;
      }
    },
    onSearch(query) {
      this.searchQuery = query;
      this.fetchProducts();
    },
    async selectFood(food) {
      this.selectedFood = null;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/foods/products/${food.id}/`);
        const detail = response.data;
        this.selectedFood = {
          id: detail.id,
          name: detail.name,
          allergens: detail.allergens,
          nutrition: {
            calories: detail.calories,
            proteins: detail.protein,
            fats: detail.fat,
            carbs: detail.carbs,
            fiber: detail.fiber,
            sugar: detail.sugar,
            sodium: detail.sodium
          }
        };
        this.amount = 100;
      }
      catch (e) {
        console.error('Error fetching product details:', e);
        this.error = 'Не вдалося завантажити деталі продукту';
      }
      finally {
        this.isLoading = false;
      }
    },
    addToMeal() {
      if (this.selectedFood && this.amount > 0) {
        const foodWithAmount = {
          ...this.selectedFood,
          amount: this.amount,
          calculated: {
            calories: (this.selectedFood.nutrition.calories * this.amount) / 100,
            proteins: (this.selectedFood.nutrition.proteins * this.amount) / 100,
            fats: (this.selectedFood.nutrition.fats * this.amount) / 100,
            carbs: (this.selectedFood.nutrition.carbs * this.amount) / 100,
            fiber: (this.selectedFood.nutrition.fiber * this.amount) / 100,
            sugar: (this.selectedFood.nutrition.sugar * this.amount) / 100,
            sodium: (this.selectedFood.nutrition.sodium * this.amount) / 100
          }
        };
        this.$emit('add-food', foodWithAmount);
      }
    },
    handleEscape(e) {
      if (e.key === 'Escape') {
        this.$emit('close');
      }
    }
  }
};
</script> 
