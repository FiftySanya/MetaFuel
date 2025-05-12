<template>
  <section class="mb-8 bg-white rounded-lg shadow-md overflow-hidden">
    <table class="min-w-full">
      <thead class="bg-blue-50 text-gray-700">
        <tr>
          <th class="p-4 text-left font-semibold">Прийом їжі</th>
          <th class="p-4 text-center font-semibold">Калорії</th>
          <th class="p-4 text-center font-semibold">Білки</th>
          <th class="p-4 text-center font-semibold">Жири</th>
          <th class="p-4 text-center font-semibold">Вуглеводи</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(data, key) in nutritionData" :key="key" class="border-b border-gray-200">
          <td class="p-4">{{ mealLabels[key] }}</td>
          <td class="p-4 text-center">{{ formatValue(data.calories) }}</td>
          <td class="p-4 text-center">{{ formatValue(data.proteins) }}</td>
          <td class="p-4 text-center">{{ formatValue(data.fats) }}</td>
          <td class="p-4 text-center">{{ formatValue(data.carbs) }}</td>
        </tr>
        <tr class="bg-gray-50 font-semibold text-gray-800">
          <td class="p-4">Всього</td>
          <td class="p-4 text-center">{{ formatValue(total.calories) }}</td>
          <td class="p-4 text-center">{{ formatValue(total.proteins) }}</td>
          <td class="p-4 text-center">{{ formatValue(total.fats) }}</td>
          <td class="p-4 text-center">{{ formatValue(total.carbs) }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script>
export default {
  name: 'SummaryTable',
  props: {
    nutritionData: {
      type: Object,
      required: true
    }
  },
  computed: {
    mealLabels() {
      return {
        breakfast: 'Сніданок',
        lunch: 'Обід',
        dinner: 'Вечеря',
        snack: 'Перекус'
      };
    },
    total() {
      return Object.values(this.nutritionData).reduce(
        (acc, curr) => {
          acc.calories += curr.calories || 0;
          acc.proteins += curr.proteins || 0;
          acc.fats += curr.fats || 0;
          acc.carbs += curr.carbs || 0;
          return acc;
        },
        { calories: 0, proteins: 0, fats: 0, carbs: 0 }
      );
    }
  },
  methods: {
    formatValue(value) {
      const rounded = Math.round(value * 10) / 10;
      return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
    }
  }
};
</script> 