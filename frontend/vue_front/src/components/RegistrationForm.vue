<template>
  <section class="w-full max-w-md">
    <h2 class="mb-6 text-2xl font-bold text-gray-800">
      Створіть свій обліковий запис
    </h2>

    <form @submit.prevent="handleSubmit" class="flex flex-col gap-4" autocomplete="off">
      <div class="mb-4">
        <input
          autocomplete="off"
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
          autocomplete="email"
          type="email"
          placeholder="Електронна адреса"
          v-model="email"
          required
          class="w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          :class="{ 'border-red-500': errors.email }"
        />
        <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
      </div>

      <div class="mb-4">
        <input
          autocomplete="new-password"
          type="password"
          placeholder="Пароль"
          v-model="password1"
          required
          class="w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          :class="{ 'border-red-500': errors.password1 }"
        />
        <p v-if="errors.password1" class="mt-1 text-sm text-red-600">{{ errors.password1 }}</p>
      </div>

      <div class="mb-4">
        <input
          autocomplete="new-password"
          type="password"
          placeholder="Підтвердження пароля"
          v-model="password2"
          required
          class="w-full px-4 py-3 text-gray-800 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          :class="{ 'border-red-500': errors.password2 }"
        />
        <p v-if="errors.password2" class="mt-1 text-sm text-red-600">{{ errors.password2 }}</p>
      </div>

      <div class="flex items-center mt-2 mb-4">
        <input
          id="terms"
          type="checkbox"
          v-model="agreedToTerms"
          class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="terms" class="ml-2 text-sm text-gray-600">
          Я погоджуюсь з <router-link to="/terms" class="text-blue-600 hover:underline">умовами користування</router-link>
        </label>
      </div>

      <button
        type="submit"
        class="flex items-center justify-center gap-3 px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-full shadow-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mt-4"
      >
        <span>Реєструйся</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </button>

      <div v-if="apiError" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
        {{ apiError }}
      </div>

      <div class="mt-4 text-center">
        <p class="text-sm text-gray-600">
          Вже маєте обліковий запис?
          <router-link to="/login" class="text-blue-600 hover:underline font-medium">
            Увійти
          </router-link>
        </p>
      </div>
    </form>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: "RegistrationForm",
  
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      password2: "",

      agreedToTerms: false,
      isLoading: false,

      apiError: "",
      errors: {
        username: "",
        email: "",
        password1: "",
        password2: "",
      },
    };
  },

  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        username: "",
        email: "",
        password1: "",
        password2: "",
      };

      if (!this.username) {
        this.errors.username = "Введіть ім'я користувача";
        isValid = false;
      }

      if (!this.email) {
        this.errors.email = "Введіть адресу електронної пошти";
        isValid = false;
      } 
      else if (!/\S+@\S+\.\S+/.test(this.email)) {
        this.errors.email = "Введіть коректну адресу електронної пошти";
        isValid = false;
      }

      if (!this.password1) {
        this.errors.password1 = "Введіть пароль";
        isValid = false;
      } 
      else if (this.password1.length < 8) {
        this.errors.password1 = "Пароль має містити щонайменше 8 символів";
        isValid = false;
      }

      if (this.password1 !== this.password2) {
        this.errors.password2 = "Паролі не співпадають";
        isValid = false;
      }

      if (!this.agreedToTerms) {
        alert("Будь ласка, прийміть умови користування");
        isValid = false;
      }

      return isValid;
    },
    
    async handleSubmit() {
      if (!this.validateForm()) return;

      this.isLoading = true;
      this.apiError = "";
      
      try {
        await axios.post('/auth/registration/', {
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2
        });
        
        this.$router.push('/dashboard');
      } 
      catch (error) {
        console.error("Registration error:", error);
        
        if (error.response && error.response.data) {
          if (error.response.data.username) {
            this.errors.username = error.response.data.username[0];
          }
          
          if (error.response.data.email) {
            this.errors.email = error.response.data.email[0];
          }
          
          if (error.response.data.password1) {
            this.errors.password1 = error.response.data.password1[0];
          }
          
          if (error.response.data.password2) {
            this.errors.password2 = error.response.data.password2[0];
          }
          
          if (error.response.data.non_field_errors) {
            this.apiError = error.response.data.non_field_errors[0];
          }
        } 
        else {
          this.apiError = "Не вдалося підключитися до сервера. Перевірте ваше інтернет-з'єднання";
        }
      } 
      finally {
        this.isLoading = false;
      }
    },
  },
};
</script> 
