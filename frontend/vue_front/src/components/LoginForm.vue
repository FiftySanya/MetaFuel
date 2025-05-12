<template>
  <section class="w-full max-w-md">
    <h2 class="mb-6 text-2xl font-bold text-gray-800">
      Увійдіть або зареєструйтеся за лічені секунди
    </h2>

    <form @submit.prevent="handleSubmit" class="flex flex-col gap-4" autocomplete="on">
      <div class="mb-4">
        <input
          autocomplete="username"
          type="text"
          placeholder="Ім'я користувача"
          v-model="username"
          required
          class="w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          :class="{ 'border-red-500': errors.username }"
        />
        <p v-if="errors.username" class="mt-1 text-sm text-red-600">{{ errors.username }}</p>
      </div>

      <div class="mb-4">
        <input
          autocomplete="current-password"
          type="password"
          placeholder="Пароль"
          v-model="password"
          required
          class="w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          :class="{ 'border-red-500': errors.password }"
        />
        <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
      </div>

      <div class="flex justify-between mt-2 mb-4">
        <div class="flex items-center">
          <input
            id="remember"
            type="checkbox"
            v-model="rememberMe"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label for="remember" class="ml-2 text-sm text-gray-600">Запам'ятати мене</label>
        </div>
      </div>

      <button
        type="submit"
        class="flex items-center justify-center gap-3 px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-full shadow-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mt-4"
      >
        <span>Увійти</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
        </svg>
      </button>

      <div v-if="apiError" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
        {{ apiError }}
      </div>

      <div class="mt-4 text-center">
        <p class="text-sm text-gray-600">
          Ще не маєте облікового запису?
          <router-link to="/register" class="text-blue-600 hover:underline font-medium">
            Зареєструйтеся
          </router-link>
        </p>
      </div>
    </form>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
      rememberMe: false,
      isLoading: false,
      apiError: "",
      errors: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        username: "",
        password: "",
      };

      if (!this.username) {
        this.errors.username = "Введіть ім'я користувача";
        isValid = false;
      }

      if (!this.password) {
        this.errors.password = "Введіть пароль";
        isValid = false;
      }

      return isValid;
    },
    async handleSubmit() {
      if (!this.validateForm()) return;

      this.isLoading = true;
      this.apiError = "";
      
      try {
        await axios.post('/auth/login/', {
          username: this.username,
          password: this.password
        });
        
        this.$router.push('/dashboard');
      }
      catch (error) {
        console.error("Login error:", error);
        
        if (error.response && error.response.data) {
          if (error.response.data.non_field_errors) {
            this.apiError = error.response.data.non_field_errors[0];
          }
          else if (error.response.data.detail) {
            this.apiError = error.response.data.detail;
          }
          else {
            this.apiError = "Сталася помилка при вході. Перевірте ваші дані.";
          }
        }
        else {
          this.apiError = "Не вдалося підключитися до сервера. Перевірте ваше інтернет-з'єднання.";
        }
      }
      finally {
        this.isLoading = false;
      }
    },
  },
};
</script> 
