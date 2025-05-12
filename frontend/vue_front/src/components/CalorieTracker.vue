<template>
  <section class="bg-white p-6 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-4">
      <h3 class="mb-0 text-xl font-semibold text-gray-800">Трекер калорій</h3>
      <button
        @click="goToFood"
        class="text-blue-600 font-medium hover:text-blue-800 transition-colors"
      >+ Додати їжу</button>
    </div>
    
    <div class="flex justify-between items-center mb-6">
      <div class="text-center">
        <p class="text-3xl font-bold text-blue-600">{{ formatValue(consumedCalories) }}</p>
        <p class="text-sm text-gray-600">з {{ formatValue(calorieGoal) }} ккал</p>
      </div>
      <div class="h-16 w-16 rounded-full border-4 border-blue-100 flex items-center justify-center">
        <span class="text-lg font-semibold text-blue-800">{{ progressPercentage }}%</span>
      </div>
    </div>

    <div class="mt-4 bg-gray-200 h-2 rounded-full overflow-hidden">
      <div 
        class="bg-blue-600 h-full rounded-full" 
        :style="{ width: `${Math.min(progressPercentage, 100)}%` }"
      ></div>
    </div>
    <div v-if="isLoading" class="flex justify-center my-4">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    <div v-else-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg my-4">
      {{ error }}
    </div>
    <div v-else-if="consumedCalories > 0" class="mt-6">
      <SummaryTable :nutritionData="nutritionData" />
    </div>
    <div v-else class="mt-6 text-center text-gray-500 p-4 bg-gray-50 rounded-lg">
      <p class="m-0">Сьогодні ще не додано жодної їжі</p>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import SummaryTable from '@/components/SummaryTable.vue';
export default {
  name: "CalorieTracker",
  components: { SummaryTable },
  props: {
    date: {
      type: String,
      required: true
    },
    calorieGoal: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      consumedCalories: 0,
      isLoading: false,
      error: null,
      nutritionData: {
        breakfast: { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        lunch:     { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        dinner:    { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        snack:     { calories: 0, proteins: 0, fats: 0, carbs: 0 }
      }
    };
  },
  methods: {
    goToFood() {
      this.$router.push({ name: 'Food' });
    },
    formatValue(value) {
      const rounded = Math.round(value * 10) / 10;
      return Number.isInteger(rounded) ? rounded.toString() : rounded.toFixed(1);
    },
    async fetchMeals() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/foods/meals/', { params: { date: this.date } });
        let total = 0;
        const summary = {
          breakfast: { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          lunch:     { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          dinner:    { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          snack:     { calories: 0, proteins: 0, fats: 0, carbs: 0 }
        };
        response.data.forEach(meal => {
          if (meal.meal_type in summary) {
            meal.items.forEach(item => {
              total += item.calories || 0;
              const m = summary[meal.meal_type];
              m.calories += item.calories || 0;
              m.proteins += item.protein  || 0;
              m.fats     += item.fat      || 0;
              m.carbs    += item.carbs    || 0;
            });
          }
        });
        this.consumedCalories = total;
        this.nutritionData = summary;
      }
      catch (e) {
        console.error('Error fetching calorie data:', e);
        this.error = 'Не вдалося завантажити дані про калорії';
        this.consumedCalories = 0;
      }
      finally {
        this.isLoading = false;
      }
    }
  },
  computed: {
    progressPercentage() {
      if (!this.calorieGoal || this.calorieGoal === 0) {
        return 0;
      }
      const pct = (this.consumedCalories / this.calorieGoal) * 100;
      return Math.round(pct);
    }
  },
  watch: {
    date: { handler: 'fetchMeals', immediate: true }
  }
};
</script> 
