<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 bg-gray-800/50 backdrop-blur-md">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6 md:p-8 relative">
      <button @click="$emit('cancel')" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl">
        &times;
      </button>
      <div class="mb-4 text-center">
        <h2 class="text-xl font-semibold text-gray-800">Налаштування плану</h2>
      </div>

      <div class="flex justify-center space-x-2 mb-6">
        <span
          v-for="n in 3"
          :key="n"
          class="w-2 h-2 rounded-full"
          :class="step === n ? 'bg-blue-600' : 'bg-gray-300'"
        ></span>
      </div>

      <div v-if="step === 1" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Вік (18-60)</label>
          <input
            v-model.number="form.age"
            type="number"
            min="18"
            max="60"
            class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Ріст (см)</label>
          <input
            v-model.number="form.height"
            type="number"
            min="100"
            max="250"
            class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Вага (кг)</label>
          <input
            v-model.number="form.initial_weight"
            type="number"
            min="30"
            max="200"
            class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Стать</label>
          <div class="flex items-center space-x-6 mt-1">
            <label class="flex items-center space-x-2">
              <input type="radio" v-model="form.gender" value="male" class="h-4 w-4 text-blue-600" />
              <span class="text-gray-700">Чоловік</span>
            </label>
            <label class="flex items-center space-x-2">
              <input type="radio" v-model="form.gender" value="female" class="h-4 w-4 text-blue-600" />
              <span class="text-gray-700">Жінка</span>
            </label>
          </div>
        </div>
      </div>

      <div v-if="step === 2" class="space-y-4">
        <label class="block text-sm font-medium text-gray-700">Рівень активності</label>
        <div class="grid grid-cols-1 gap-3">
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.activity_level" value="sedentary" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Сидячий</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.activity_level" value="light" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Легко активний</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.activity_level" value="moderate" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Помірно активний</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.activity_level" value="active" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Дуже активний</span>
          </label>
        </div>
      </div>

      <div v-if="step === 3" class="space-y-4">
        <label class="block text-sm font-medium text-gray-700">Ваша ціль</label>
        <div class="grid grid-cols-1 gap-3">
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.goal_type" value="maintain" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Підтримувати вагу</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.goal_type" value="lose" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Схуднення на 2 кг/місяць</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" v-model="form.goal_type" value="gain" class="h-4 w-4 text-blue-600" />
            <span class="text-gray-700">Набір 2 кг/місяць</span>
          </label>
        </div>
      </div>

      <div class="mt-6 flex justify-between">
        <button
          @click="prevStep"
          :disabled="step === 1"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50"
        >
          Назад
        </button>
        <button
          v-if="step < 3"
          @click="nextStep"
          :disabled="!canProceed"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          Далі
        </button>
        <button
          v-else
          @click="finish"
          :disabled="!canProceed"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          Готово
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'PlanSetupWizard',
  data() {
    return {
      step: 1,
      form: {
        age: null,
        height: null,
        initial_weight: null,
        gender: '',
        activity_level: '',
        goal_type: ''
      }
    };
  },
  computed: {
    canProceed() {
      if (this.step === 1) {
        return (
          this.form.age >= 18 && this.form.age <= 60 &&
          this.form.height >= 140 && this.form.height <= 210 &&
          this.form.initial_weight >= 40 && this.form.initial_weight <= 150 &&
          this.form.gender
        );
      }
      if (this.step === 2) {
        return !!this.form.activity_level;
      }
      if (this.step === 3) {
        return !!this.form.goal_type;
      }
      return false;
    }
  },
  methods: {
    nextStep() {
      if (this.canProceed && this.step < 3) this.step++;
    },
    prevStep() {
      if (this.step > 1) this.step--;
    },
    async finish() {
      if (!this.canProceed) return;

      const weight = this.form.initial_weight;
      const age = this.form.age;
      const height = this.form.height;
      const gender = this.form.gender;
      const activity = this.form.activity_level;
      const goalType = this.form.goal_type;

      let bmr;
      if (gender === 'male') {
        bmr = 10 * weight + 6.25 * height - 5 * age + 5;
      } 
      else {
        bmr = 10 * weight + 6.25 * height - 5 * age - 161;
      }

      const mult = { sedentary:1.2, light:1.375, moderate:1.55, active:1.725 };
      const tdee = bmr * (mult[activity] || 1.2);

      const exercise_calorie_goal = Math.round(tdee - bmr);

      let intake;
      if (goalType === 'maintain') intake = tdee;
      else if (goalType === 'lose') intake = tdee - 510;
      else intake = tdee + 510;
      const calorie_intake_goal = Math.round(intake);

      let goal_weight;
      if (goalType === 'maintain') goal_weight = weight;
      else if (goalType === 'lose') goal_weight = weight - 2;
      else goal_weight = weight + 2;

      try {
        const payload = {
          initial_weight: weight,
          goal_weight: goal_weight,
          calorie_intake_goal: calorie_intake_goal,
          exercise_calorie_goal: exercise_calorie_goal
        };
        const response = await axios.post('/api/plans/plans/', payload);
        this.$emit('plan-created', response.data);
      } 
      catch (e) {
        console.error('Error creating plan', e);
      }
    }
  }
};
</script> 
