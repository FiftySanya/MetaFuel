<template>
  <section class="flex justify-center items-center py-4 my-4">
    <label class="mr-4 text-xl font-medium text-gray-700">Оберіть дату:</label>
    <div class="flex gap-3 items-center p-2 bg-white rounded-lg shadow border border-gray-200">
      <button @click="navigateDate(-1)" aria-label="Previous date" class="p-1 hover:bg-gray-100 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <span class="text-xl font-medium text-gray-800">{{ formattedDate }}</span>
      <button @click="navigateDate(1)" aria-label="Next date" :disabled="isNextDisabled" class="p-1 hover:bg-gray-100 rounded-full disabled:opacity-50 disabled:cursor-not-allowed">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script>
export default {
  name: "DateSelector",
  data() {
    return {
      currentDate: new Date(),
    };
  },
  computed: {
    formattedDate() {
      const months = [
        "СІЧНЯ",
        "ЛЮТОГО",
        "БЕРЕЗНЯ",
        "КВІТНЯ",
        "ТРАВНЯ",
        "ЧЕРВНЯ",
        "ЛИПНЯ",
        "СЕРПНЯ",
        "ВЕРЕСНЯ",
        "ЖОВТНЯ",
        "ЛИСТОПАДА",
        "ГРУДНЯ",
      ];

      const day = this.currentDate.getDate();
      const month = months[this.currentDate.getMonth()];
      const year = this.currentDate.getFullYear();

      return `${day} ${month} ${year}`;
    },
    isNextDisabled() {
      const today = new Date();
      today.setHours(0,0,0,0);
      const cur = new Date(this.currentDate);
      cur.setHours(0,0,0,0);
      return cur.getTime() >= today.getTime();
    }
  },
  methods: {
    navigateDate(days) {
      const newDate = new Date(this.currentDate);
      newDate.setDate(newDate.getDate() + days);
      const today = new Date(); today.setHours(0,0,0,0);
      newDate.setHours(0,0,0,0);
      if (newDate.getTime() > today.getTime()) return;
      this.currentDate = newDate;
      this.$emit('date-changed', this.currentDate);
    },
  },
};
</script> 
