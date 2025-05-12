<template>
  <section class="bg-white rounded-lg shadow-md p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-semibold text-gray-800">Трекер вправ</h3>
      <button
        @click="goToExercises"
        class="text-blue-600 font-medium hover:text-blue-800 transition-colors"
      >
        + Додати вправу
      </button>
    </div>

    <div class="flex justify-between items-center mb-6">
      <div class="text-center">
        <p class="text-3xl font-bold text-blue-600">{{ totalCaloriesBurned }}</p>
        <p class="text-sm text-gray-600">з {{ exerciseGoal }} ккал</p>
      </div>
      <div class="h-16 w-16 rounded-full border-4 border-blue-100 flex items-center justify-center">
        <span class="text-lg font-semibold text-blue-800">{{ exercisePercentage }}%</span>
      </div>
    </div>

    <div class="mt-4 bg-gray-200 h-2 rounded-full overflow-hidden">
      <div 
        class="bg-blue-600 h-full rounded-full" 
        :style="{ width: `${Math.min(exercisePercentage, 100)}%` }"
      ></div>
    </div>

    <div v-if="isLoading" class="flex justify-center my-4">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    <div v-else-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg my-4">
      {{ error }}
    </div>
    <div v-else>
      <div v-if="exercises.length > 0" class="mt-6">
        <div class="overflow-hidden shadow-md rounded-lg bg-white">
          <div class="grid grid-cols-4 bg-blue-50 text-gray-700 border-b border-gray-200">
            <div class="p-4 font-semibold">Назва</div>
            <div class="p-4 font-semibold">Тип</div>
            <div class="p-4 font-semibold text-center">Хвилини</div>
            <div class="p-4 font-semibold text-center">Калорії</div>
          </div>

          <div v-for="(ex, idx) in exercises" :key="idx" class="grid grid-cols-4 border-b border-gray-200">
            <div class="p-4 text-gray-800">{{ ex.exercise_details?.name || '—' }}</div>
            <div class="p-4 text-gray-600">{{ formatExerciseType(ex.exercise_details?.type) }}</div>
            <div class="p-4 text-gray-600 text-center">{{ ex.duration }}</div>
            <div class="p-4 text-gray-600 text-center">{{ ex.calories_burned }}</div>
          </div>

          <div class="grid grid-cols-4 bg-gray-50 font-semibold text-gray-800">
            <div class="p-4">Всього</div>
            <div class="p-4">—</div>
            <div class="p-4 text-center">{{ totalDuration }}</div>
            <div class="p-4 text-center">{{ totalCaloriesBurned }}</div>
          </div>
        </div>
      </div>
      <div v-else class="mt-6 text-center text-gray-500 p-4 bg-gray-50 rounded-lg">
        <p class="m-0">Сьогодні ще не додано жодної вправи</p>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: "ExerciseTracker",
  props: {
    date: {
      type: String,
      default: () => new Date().toISOString().split('T')[0]
    },
    exerciseGoal: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      exercises: [],
      isLoading: false,
      error: null
    };
  },
  computed: {
    totalCaloriesBurned() {
      if (!this.exercises || this.exercises.length === 0) return 0;
      return this.exercises.reduce((total, exercise) => total + (Number(exercise.calories_burned) || 0), 0);
    },
    totalDuration() {
      if (!this.exercises || this.exercises.length === 0) return 0;
      return this.exercises.reduce((sum, ex) => sum + (Number(ex.duration) || 0), 0);
    },
    exercisePercentage() {
      if (!this.exerciseGoal || this.exerciseGoal <= 0) return 0;
      return Math.round((this.totalCaloriesBurned / this.exerciseGoal) * 100);
    }
  },
  watch: {
    date: {
      handler: 'fetchExercises',
      immediate: true
    }
  },
  methods: {
    async fetchExercises() {
      try {
        this.isLoading = true;
        this.error = null;

        const response = await axios.get('/api/exercises/exercise-items/', {
          params: { date: this.date }
        });

        this.exercises = Array.isArray(response.data) ? response.data : [];
      }
      catch (error) {
        console.error('Error fetching exercises:', error);
        this.error = 'Не вдалося завантажити вправи';
        this.exercises = [];
      } 
      finally {
        this.isLoading = false;
      }
    },
    goToExercises() {
      this.$router.push({ name: 'Exercise' });
    },
    formatExerciseType(type) {
      const typeMap = {
        'аеробна': 'Аеробна',
        'силова': 'Силова',
        'розтяжка': 'Розтяжка',
      };
      return typeMap[type] || type || 'Не вказано';
    }
  }
};
</script> 
