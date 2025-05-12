<template>
  <section class="mb-6 bg-white rounded-lg shadow-md overflow-hidden">
    <div class="flex justify-between items-center p-4 bg-blue-50">
      <h2 class="text-xl font-semibold text-gray-800">{{ title }}</h2>
      <button
        @click="$emit('add-item')"
        class="px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg transition-colors font-medium"
      >
        Додати
      </button>
    </div>

    <div class="overflow-hidden shadow-md rounded-lg bg-white">
      <div v-if="items.length > 0" class="grid grid-cols-7 bg-gray-50 text-gray-700 border-b border-gray-200">
        <div class="p-4 font-medium">Назва</div>
        <div class="p-4 font-medium text-center">Кількість</div>
        <div class="p-4 font-medium text-center">Калорії</div>
        <div class="p-4 font-medium text-center">Білки</div>
        <div class="p-4 font-medium text-center">Жири</div>
        <div class="p-4 font-medium text-center">Вуглеводи</div>
        <div class="p-4 font-medium text-center">Дії</div>
      </div>

      <div v-if="isLoading" class="p-6 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
      </div>

      <div v-else-if="items.length === 0" class="p-6 text-center text-gray-500">
        Додайте продукти до прийому їжі
      </div>

      <div v-else>
        <div v-for="(item, index) in items" :key="item.id" class="grid grid-cols-7 border-b border-gray-200">
          <div class="p-4 text-gray-800">{{ item.name }}</div>
          <div class="p-4 text-gray-600 text-center">{{ item.amount }}г</div>
          <div class="p-4 text-gray-600 text-center">{{ item.calculated ? item.calculated.calories : item.nutrition.calories }}</div>
          <div class="p-4 text-gray-600 text-center">{{ item.calculated ? item.calculated.proteins : item.nutrition.proteins }}</div>
          <div class="p-4 text-gray-600 text-center">{{ item.calculated ? item.calculated.fats : item.nutrition.fats }}</div>
          <div class="p-4 text-gray-600 text-center">{{ item.calculated ? item.calculated.carbs : item.nutrition.carbs }}</div>
          <div class="p-4 text-center" @click.stop>
            <button @click="removeItem(index)" class="text-red-500 hover:text-red-700" aria-label="Remove item">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'MealSection',
  props: {
    title: {
      type: String,
      required: true
    },
    items: {
      type: Array,
      default: () => []
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
    }
  },
  methods: {
    removeItem(index) {
      this.$emit('remove-item', { mealType: this.title, index });
    }
  },
  computed: {
  }
};
</script> 
