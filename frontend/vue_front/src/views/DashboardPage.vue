<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <div class="container mx-auto px-4 py-8">
      <section class="mb-10">
        <div class="flex justify-between items-center mb-3">
          <h2 class="m-0 text-4xl font-bold text-blue-800">Вітаю, {{ username }}</h2>
          <button
            @click="showPlanWizard = true"
            class="px-6 py-3 transform translate-y-8 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700 transition-colors"
          >
            Обрати план
          </button>
        </div>
        <h3 class="m-0 text-2xl font-medium text-gray-800">Твій план на сьогодні:</h3>
      </section>

      <PlanSetupWizard v-if="showPlanWizard" @plan-created="onPlanCreated" @cancel="showPlanWizard = false" />
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <CalorieTracker 
          :date="currentDate"
          :calorieGoal="dailyGoals.calories"
        />
        <ExerciseTracker 
          :date="currentDate"
          :exerciseGoal="user.exerciseGoal"
        />
      </div>
      
      <div class="mb-8">
        <div class="p-6 bg-white rounded-lg shadow-md">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Денний прогрес</h2>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700 mb-2">Калорії</h3>
              <p class="text-2xl font-bold text-blue-800">{{ formatNumber(consumedCalories) }} / {{ formatNumber(dailyGoals.calories) }}</p>
              <div class="mt-2 bg-gray-200 h-2 rounded-full overflow-hidden">
                <div 
                  class="bg-blue-600 h-full rounded-full" 
                  :style="{ width: `${Math.min((consumedCalories / dailyGoals.calories) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700 mb-2">Білки</h3>
              <p class="text-2xl font-bold text-blue-800">{{ formatNumber(macronutrients.proteins || 0) }} / {{ formatNumber(macroTargets.proteinsGram) }}</p>
              <div class="mt-2 bg-gray-200 h-2 rounded-full overflow-hidden">
                <div 
                  class="bg-blue-600 h-full rounded-full" 
                  :style="{ width: `${Math.min(((macronutrients.proteins || 0) / macroTargets.proteinsGram) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700 mb-2">Жири</h3>
              <p class="text-2xl font-bold text-blue-800">{{ formatNumber(macronutrients.fats || 0) }} / {{ formatNumber(macroTargets.fatsGram) }}</p>
              <div class="mt-2 bg-gray-200 h-2 rounded-full overflow-hidden">
                <div 
                  class="bg-blue-600 h-full rounded-full" 
                  :style="{ width: `${Math.min(((macronutrients.fats || 0) / macroTargets.fatsGram) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700 mb-2">Вуглеводи</h3>
              <p class="text-2xl font-bold text-blue-800">{{ formatNumber(macronutrients.carbs || 0) }} / {{ formatNumber(macroTargets.carbsGram) }}</p>
              <div class="mt-2 bg-gray-200 h-2 rounded-full overflow-hidden">
                <div 
                  class="bg-blue-600 h-full rounded-full" 
                  :style="{ width: `${Math.min(((macronutrients.carbs || 0) / macroTargets.carbsGram) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
          </div>

          <div :class="`mt-6 p-4 rounded-lg ${caloricBalanceStatus}`">
            <p class="text-xl font-medium text-gray-700">Енергетичний баланс</p>
            <p class="text-2xl font-bold mt-1">{{ formatNumber(caloricBalanceCurrent) }} / {{ formatNumber(caloricBalanceGoal) }}</p>
          </div>

          <div class="mt-6 flex items-center space-x-6">
            <label class="text-xl font-semibold text-gray-700">Ваша вага сьогодні:</label>
            <input
              v-model.number="todayWeight"
              @blur="formatWeight"
              type="number"
              step="0.01"
              class="w-32 px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-base"
            />
            <span class="text-xl font-semibold text-gray-700">кг</span>
            <button
              @click="submitWeightLog"
              :class="[
                'px-6 py-2 text-white text-base rounded-lg font-medium transition-colors',
                weightLogged ? 'bg-green-600 hover:bg-green-700' : 'bg-blue-600 hover:bg-blue-700'
              ]"
            >
              {{ weightLogged ? 'Збережено' : 'Зберегти' }}
            </button>
          </div>
        </div>
      </div>
      
      <div>
        <section class="flex justify-between items-center bg-white p-6 rounded-lg shadow-md">
          <p class="text-lg text-gray-800">
            Побачити пройдений шлях можна тут
          </p>
          <router-link
            to="/reports"
            class="px-6 py-3 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg transition-colors text-center font-medium"
          >
            Переглянути звіт
          </router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import CalorieTracker from '@/components/CalorieTracker.vue';
import ExerciseTracker from '@/components/ExerciseTracker.vue';
import PlanSetupWizard from '@/components/PlanSetupWizard.vue';
import axios from 'axios';

export default {
  name: 'DashboardPage',
  components: {
    AppHeader,
    CalorieTracker,
    ExerciseTracker,
    PlanSetupWizard
  },
  data() {
    return {
      username: '',
      currentDate: (() => {
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
      })(),
      dailyGoals: {
        calories: 0
      },
      consumedCalories: 0,
      macronutrients: {
        proteins: 0,
        fats: 0,
        carbs: 0
      },
      user: {
        exerciseGoal: 0,
        exerciseCompleted: 0
      },
      currentPlan: null,
      showPlanWizard: false,
      todayWeight: null,
      weightLogged: false,
    };
  },
  computed: {
    caloricBalanceCurrent() {
      return this.consumedCalories - (Number(this.user.exerciseCompleted) || 0);
    },
    caloricBalanceGoal() {
      return this.dailyGoals.calories - this.user.exerciseGoal;
    },
    caloricBalanceStatus() {
      const curr = this.caloricBalanceCurrent;
      const goal = this.caloricBalanceGoal;
      if (curr < 0) return 'bg-red-100 text-red-700';
      if (goal && curr > goal) return 'bg-yellow-100 text-yellow-700';
      return 'bg-green-100 text-green-700';
    },
    macroTargets() {
      const total = this.dailyGoals.calories;
      const proteinCals = total * 0.2;
      const fatsCals = total * 0.3;
      const carbsCals = total * 0.5;
      return {
        proteinsGram: Math.round(proteinCals / 4),
        fatsGram: Math.round(fatsCals / 9),
        carbsGram: Math.round(carbsCals / 4)
      };
    }
  },
  async created() {
    await this.loadUser();
    await this.loadCurrentPlan();
    await this.initializeData();
    await this.loadTodayWeightLog();
  },
  methods: {
    async initializeData() {
      await this.fetchNutritionData();
      await this.fetchUserExercises();
    },
    async loadUser() {
      try {
        const res = await axios.get('/api/users/me/');
        this.username = res.data.username || res.data.email || '';
      } 
      catch (e) {
        console.error('Error loading user profile:', e);
        this.username = '';
      }
    },
    async loadTodayWeightLog() {
      if (!this.currentPlan) return;
      try {
        const res = await axios.get('/api/plans/days/', {
          params: { plan: this.currentPlan.id, date: this.currentDate }
        });
        const day = Array.isArray(res.data) && res.data.length > 0 ? res.data[0] : null;
        if (day && day.weight_gained != null) {
          this.todayWeight = Number(day.weight_gained);
          this.weightLogged = true;
        }
      }
      catch (e) {
        console.error("Error loading today's weight:", e);
      }
    },
    async submitWeightLog() {
      if (this.todayWeight == null || !this.currentPlan) return;
      try {
        const res = await axios.get('/api/plans/days/', {
          params: { plan: this.currentPlan.id, date: this.currentDate }
        });
        let day = Array.isArray(res.data) && res.data.length > 0 ? res.data[0] : null;
        if (day) {
          await axios.patch(`/api/plans/days/${day.id}/`, { weight_gained: this.todayWeight });
        }
        else {
          const createRes = await axios.post('/api/plans/days/', {
            plan: this.currentPlan.id,
            date: this.currentDate,
            weight_gained: this.todayWeight
          });
          day = createRes.data;
        }
        await this.loadTodayWeightLog();
      }
      catch (e) {
        console.error("Error saving today's weight:", e);
      }
    },
    async loadCurrentPlan() {
      try {
        const res = await axios.get('/api/plans/plans/', {
          params: { is_active: true }
        });
        const plans = res.data;
        if (plans.length > 0) {
          this.currentPlan = plans[0];
          this.dailyGoals.calories = this.currentPlan.calorie_intake_goal;
          this.user.exerciseGoal = this.currentPlan.exercise_calorie_goal;
        }
        else {
          this.currentPlan = null;
          this.showPlanWizard = true;
        }
      }
      catch (e) {
        console.error('Error loading active plan:', e);
        this.showPlanWizard = true;
      }
    },
    async fetchNutritionData() {
      try {
        const response = await axios.get('/api/foods/meals/', {
          params: { date: this.currentDate }
        });
        let totalCalories = 0;
        let totalProteins = 0;
        let totalFats = 0;
        let totalCarbs = 0;
        response.data.forEach(meal => {
          meal.items.forEach(item => {
            totalCalories += item.calories || 0;
            totalProteins += item.protein  || 0;
            totalFats += item.fat      || 0;
            totalCarbs += item.carbs   || 0;
          });
        });
        this.macronutrients = { proteins: totalProteins, fats: totalFats, carbs: totalCarbs };
        this.consumedCalories = totalCalories;
      }
      catch (error) {
        console.error('Error fetching nutrition data:', error);
      }
    },
    async fetchUserExercises() {
      try {
        const res = await axios.get('/api/exercises/exercise-items/', {
          params: { date: this.currentDate }
        });
        const exercises = res.data;
        const burned = exercises.reduce((sum, ex) => sum + (ex.calories_burned || 0), 0);
        this.user.exerciseCompleted = burned;
      }
      catch (e) {
        console.error('Error loading user exercises:', e);
      }
    },
    async onPlanCreated(plan) {
      const oldPlan = this.currentPlan;

      this.currentPlan = plan;
      this.showPlanWizard = false;
      this.dailyGoals.calories = plan.calorie_intake_goal;
      this.user.exerciseGoal = plan.exercise_calorie_goal;

      await this.fetchNutritionData();
      await this.fetchUserExercises();

      let weightVal = null;
      if (oldPlan) {
        try {
          const oldDayRes = await axios.get('/api/plans/days/', { params: { plan: oldPlan.id, date: this.currentDate } });
          const oldDay = Array.isArray(oldDayRes.data) && oldDayRes.data.length > 0 ? oldDayRes.data[0] : null;
          weightVal = oldDay && oldDay.weight_gained != null ? oldDay.weight_gained : null;
        }
        catch (e) {
          console.error('Error fetching old plan day:', e);
        }
      }

      const payload = { plan: plan.id, date: this.currentDate };
      if (this.consumedCalories > 0)      payload.calories_consumed = this.consumedCalories;
      if (this.user.exerciseCompleted > 0) payload.calories_burned   = this.user.exerciseCompleted;
      if (weightVal != null)               payload.weight_gained     = weightVal;
      try {
        await axios.post('/api/plans/days/', payload);
      }
      catch (e) {
        console.error('Error creating new plan day:', e);
      }
      await this.loadTodayWeightLog();
    },
    formatNumber(value) {
      const num = Number(value);
      return Number.isInteger(num) ? num.toString() : num.toFixed(1);
    },
    formatWeight() {
      if (this.todayWeight != null) {
        this.todayWeight = Number(this.todayWeight.toFixed(2));
      }
    }
  }
};
</script> 
