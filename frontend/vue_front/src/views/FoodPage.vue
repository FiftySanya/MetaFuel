<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    <div class="container mx-auto px-4 py-8">
      <DateSelector @date-changed="updateDate" />
      
      <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg my-4">
        {{ error }}
      </div>
      
      <div class="mb-10">
        <MealOverview 
          v-for="(meals, mealType) in mealData" 
          :key="mealType" 
          :title="mealLabels[mealType]" 
          :items="meals"
          :isLoading="isLoading"
          @add-item="openFoodModal(mealType)"
          @remove-item="removeFood"
        />
      </div>
      
      <h2 class="text-2xl font-bold text-gray-800 text-center my-4">Підсумки дня</h2>
      
      <SummaryTable :nutritionData="nutritionData" />
      
      <FoodSelectionModal 
        v-if="showFoodModal" 
        @close="showFoodModal = false"
        @add-food="addSelectedFood"
      />
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import DateSelector from '@/components/DateSelector.vue';
import MealOverview from '@/components/MealOverview.vue';
import FoodSelectionModal from '@/components/FoodSelectionModal.vue';
import SummaryTable from '@/components/SummaryTable.vue';
import axios from 'axios';

export default {
  name: 'FoodPage',
  components: {
    AppHeader,
    DateSelector,
    MealOverview,
    SummaryTable,
    FoodSelectionModal
  },
  data() {
    return {
      selectedDate: new Date(),
      showFoodModal: false,
      currentMealType: '',
      mealData: {
        breakfast: [],
        lunch: [],
        dinner: [],
        snack: []
      },
      nutritionData: {
        breakfast: { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        lunch:     { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        dinner:    { calories: 0, proteins: 0, fats: 0, carbs: 0 },
        snack:     { calories: 0, proteins: 0, fats: 0, carbs: 0 }
      },
      isLoading: false,
      error: null
    };
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
    formattedDate() {
      const date = this.selectedDate;
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    }
  },
  created() {
    this.fetchMeals();
  },
  methods: {
    async updateDate(date) {
      this.selectedDate = date;
      await this.fetchMeals();
    },
    async fetchMeals() {
      try {
        this.isLoading = true;
        const response = await axios.get('/api/foods/meals/', {
          params: { date: this.formattedDate }
        });
        
        this.mealData = {
          breakfast: [],
          lunch: [],
          dinner: [],
          snack: []
        };
        
        response.data.forEach(meal => {
          if (meal.meal_type in this.mealData) {
            meal.items.forEach(item => {
              const product = item.product_details || {};
              this.mealData[meal.meal_type].push({
                id: item.id,
                name: product.name,
                amount: item.amount,
                nutrition: {
                  calories: item.calories,
                  proteins: item.protein,
                  fats: item.fat,
                  carbs: item.carbs
                },
                productId: product.id,
                mealId: meal.id
              });
            });
          }
        });
        
        this.nutritionData = {
          breakfast: { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          lunch:     { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          dinner:    { calories: 0, proteins: 0, fats: 0, carbs: 0 },
          snack:     { calories: 0, proteins: 0, fats: 0, carbs: 0 }
        };

        Object.entries(this.mealData).forEach(([mealType, items]) => {
          items.forEach(item => {
            const vals = item.calculated || item.nutrition;
            this.nutritionData[mealType].calories += vals.calories;
            this.nutritionData[mealType].proteins += vals.proteins;
            this.nutritionData[mealType].fats += vals.fats;
            this.nutritionData[mealType].carbs += vals.carbs;
          });
        });
      }
      catch (error) {
        console.error('Error fetching meals:', error);
        this.error = 'Не вдалося завантажити дані про харчування';
      }
      finally {
        this.isLoading = false;
      }
    },
    openFoodModal(mealType) {
      this.currentMealType = mealType;
      this.showFoodModal = true;
    },
    async addSelectedFood(food) {
      try {
        let mealId;
        const mealItems = this.mealData[this.currentMealType];
        
        if (mealItems.length > 0 && mealItems[0].mealId) {
          mealId = mealItems[0].mealId;
        }
        else {
          const mealResponse = await axios.post('/api/foods/meals/', {
            meal_type: this.currentMealType,
            date: this.formattedDate
          });
          mealId = mealResponse.data.id;
        }
        
        await axios.post(`/api/foods/meals/${mealId}/add_item/`, {
          product: food.id,
          amount: food.amount || 100
        });
        
        await this.fetchMeals();
        
        this.showFoodModal = false;
      }
      catch (error) {
        console.error('Error adding food:', error);
        this.error = 'Не вдалося додати продукт';
      }
    },
    async removeFood({ mealType, index }) {
      try {
        this.isLoading = true;
        this.error = null;
        
        const mealTypeCode = Object.keys(this.mealLabels).find(
          key => this.mealLabels[key] === mealType
        );
        
        if (!mealTypeCode) {
          console.error('Невідомий тип прийому їжі:', mealType);
          this.error = 'Невідомий тип прийому їжі';
          this.isLoading = false;
          return;
        }
        
        const item = this.mealData[mealTypeCode][index];
        
        if (item && item.mealId && item.id) {
          await axios.delete(`/api/foods/meals/${item.mealId}/remove_item/`, {
            data: { item_id: item.id }
          });
          
          await this.fetchMeals();
        }
        else {
          console.error('Cannot remove item: missing id or mealId', item);
          this.error = 'Неможливо видалити продукт: відсутній ідентифікатор';
        }
      }
      catch (error) {
        console.error('Error removing food:', error);
        this.error = 'Не вдалося видалити продукт';
      }
      finally {
        this.isLoading = false;
      }
    }
  }
};
</script> 
