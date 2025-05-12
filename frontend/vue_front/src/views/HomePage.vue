<template>
  <main class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <header class="flex justify-between items-center mb-16">
        <h1 class="text-4xl font-bold text-blue-800">MetaFuel</h1>
        <div class="space-x-4">
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-medium">Увійти</router-link>
          <router-link 
            to="/register" 
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Зареєструватися
          </router-link>
        </div>
      </header>

      <section class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
        <div>
          <h2 class="text-3xl md:text-4xl font-bold text-gray-800 mb-6">
            Контролюйте своє харчування разом з MetaFuel
          </h2>
          <p class="text-xl text-gray-600 mb-8">
            Зручна система для відстеження харчування та фізичних вправ. Аналізуйте свої звички та досягайте цілей зі здоров'я та фігури.
          </p>
          <router-link 
            to="/register" 
            class="px-8 py-3 text-xl bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
          >
            Почати безкоштовно
          </router-link>
        </div>
        <div class="flex justify-center bg-transparent">
          <img 
            :src="fireImage" 
            alt="MetaFuel" 
            class="rounded-lg bg-transparent w-1/5 h-auto"
          />
        </div>
      </section>

      <section class="py-12 mb-16">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">Наші переваги</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Відстеження харчування</h3>
            <p class="text-gray-600">Легко відстежуйте свої прийоми їжі та отримуйте детальну інформацію про калорії та поживні речовини.</p>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Аналітика прогресу</h3>
            <p class="text-gray-600">Візуалізуйте свій прогрес за допомогою графіків та звітів, щоб досягати своїх цілей.</p>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Економія часу</h3>
            <p class="text-gray-600">Зручний інтерфейс для швидкого додавання їжі та вправ без зайвих ускладнень.</p>
          </div>
        </div>
      </section>

      <footer class="py-8 border-t border-gray-200">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-600">© {{ new Date().getFullYear() }} MetaFuel. Всі права захищені.</p>
          <div class="mt-4 md:mt-0">
            <router-link to="/about" class="text-gray-600 hover:text-blue-600 mx-2">Про нас</router-link>
            <router-link to="/privacy" class="text-gray-600 hover:text-blue-600 mx-2">Конфіденційність</router-link>
            <router-link to="/terms" class="text-gray-600 hover:text-blue-600 mx-2">Умови користування</router-link>
          </div>
        </div>
      </footer>
    </div>
  </main>
</template>

<script>
import fireImage from '@/assets/fire.png';

export default {
  name: "HomePage",
  data() {
    return {
      fireImage: fireImage
    };
  },
  methods: {
  }
};
</script> 
