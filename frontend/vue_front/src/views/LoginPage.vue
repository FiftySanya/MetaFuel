<template>
  <main class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
      <div class="text-center">
        <router-link to="/">
          <h1 class="text-3xl font-bold text-blue-800">MetaFuel</h1>
        </router-link>
      </div>
      <LoginForm />
    </div>
  </main>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';

export default {
  name: 'LoginPage',
  components: {
    LoginForm
  }
};
</script> 
