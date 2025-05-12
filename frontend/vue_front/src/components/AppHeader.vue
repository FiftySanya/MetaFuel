<template>
  <header class="flex justify-between items-center px-8 py-4 bg-slate-100 shadow-md">
    <h1 class="text-3xl font-bold text-blue-800">MetaFuel</h1>
    
    <nav class="hidden md:flex gap-4">
      <router-link 
        v-for="item in navItems" 
        :key="item.path" 
        :to="item.path"
        class="px-6 py-3 text-lg font-medium text-gray-700 rounded-lg transition-colors hover:bg-blue-100"
        :class="{ 'bg-blue-200': $route.path === item.path }"
      >
        {{ item.name }}
      </router-link>
    </nav>

    <div class="flex gap-4 items-center">
      <p class="text-lg text-gray-800 mr-2 max-w-xs truncate">{{ userEmail }}</p>
      <button 
        @click="logout" 
        class="flex items-center justify-center px-6 py-2 text-lg font-medium text-gray-700 bg-gray-100 rounded-full border border-gray-300 transition-colors hover:bg-gray-200"
      >
        Вийти
      </button>
    </div>
  </header>
</template>

<script>
import axios from 'axios';

export default {
  name: "AppHeader",
  data() {
    return {
      navItems: [
        { name: 'Головна', path: '/' },
        { name: 'Їжа', path: '/food' },
        { name: 'Вправи', path: '/exercise' },
        { name: 'Звіт', path: '/reports' }
      ],
      userEmail: ''
    }
  },
  async created() {
    try {
      const res = await axios.get('/api/users/me/');
      this.userEmail = res.data.email || '';
    }
    catch (e) {
      console.error('Error loading user email in header:', e);
    }
  },
  methods: {
    async logout() {
      try {
        await axios.post('/auth/logout/');
      }
      catch (e) {
        console.error('Logout error:', e);
      }
      this.$router.push('/login');
    }
  }
}
</script> 
