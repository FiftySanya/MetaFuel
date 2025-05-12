<template>
  <div>
    <div v-if="isLoading" class="flex justify-center my-4">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    <div v-else-if="!metrics.length" class="text-center text-gray-600 py-8">
      <p>Немає даних для відображення графіку.</p>
    </div>
    <div v-else ref="chart" style="width: 100%; height: 700px;"></div>
  </div>
</template>

<script>
import axios from 'axios';
import Plotly from 'plotly.js-dist';

export default {
  name: 'ProgressCharts',
  props: {
    planId: { type: Number, required: true },
    chartType: { type: String, required: true },
    activeKey: { type: Number, required: true }
  },
  data() {
    return {
      metrics: [],
      plan: null,
      isLoading: false
    };
  },
  watch: {
    activeKey: {
      immediate: true,
      handler() {
        this.loadData();
      }
    }
  },
  methods: {
    async loadData() {
      try {
        this.isLoading = true;
        const [metricsRes, planRes] = await Promise.all([
          axios.get(`/api/plans/plans/${this.planId}/daily_metrics/`),
          axios.get(`/api/plans/plans/${this.planId}/`)
        ]);
        this.metrics = metricsRes.data;
        this.plan = planRes.data;
      } 
      catch (e) {
        console.error('Error loading metrics or plan:', e);
      }
      finally {
        this.isLoading = false;
        this.$nextTick(() => {
          if (this.$refs.chart) {
            this.drawChart();
          }
        });
      }
    },
    drawChart() {
      if (!this.metrics.length || !this.plan || !this.$refs.chart) {
        if (this.$refs.chart) {
          try { Plotly.purge(this.$refs.chart); } catch (e) {}
        }
        return;
      }
      const days = 31;
      const xAxis = Array.from({ length: days }, (_, i) => i + 1);
      const yConsumed = Array(days).fill(null);
      const yBurned = Array(days).fill(null);
      const yWeight  = Array(days).fill(null);

      this.metrics.forEach(item => {
        const diffMs = new Date(item.date) - new Date(this.plan.start_date);
        const idx = Math.round(diffMs / (1000 * 60 * 60 * 24));
        if (idx >= 0 && idx < days) {
          if (item.calories_consumed != null) {
            yConsumed[idx] = Number(item.calories_consumed);
          }
          if (item.calories_burned != null) {
            yBurned[idx]   = Number(item.calories_burned);
          }
          if (item.weight_gained != null) yWeight[idx] = Number(item.weight_gained);
        }
      });

      const traces = [];
      if (this.chartType === 'consumed') {
        const goalLine = Array(days).fill(Number(this.plan.calorie_intake_goal));
        traces.push({ x: xAxis, y: yConsumed, mode: 'lines+markers', name: 'Спожито', connectgaps: true });
        traces.push({ x: xAxis, y: goalLine, mode: 'lines', line: { dash: 'dash' }, name: 'Рекомендовано', connectgaps: true });
      }
      else if (this.chartType === 'burned') {
        const goalLine = Array(days).fill(Number(this.plan.exercise_calorie_goal));
        traces.push({ x: xAxis, y: yBurned, mode: 'lines+markers', name: 'Спалено', connectgaps: true });
        traces.push({ x: xAxis, y: goalLine, mode: 'lines', line: { dash: 'dash' }, name: 'Рекомендовано', connectgaps: true });
      }
      else if (this.chartType === 'weight') {
        const trendX = [1, days];
        const trendY = [Number(this.plan.initial_weight), Number(this.plan.goal_weight)];
        traces.push({ x: xAxis, y: yWeight, mode: 'lines+markers', name: 'Вага', connectgaps: true });
        traces.push({ x: trendX, y: trendY, mode: 'lines', line: { dash: 'dash' }, name: 'Цільова вага', connectgaps: true });
      }

      const layout = {
        margin: { t: 60, b: 80, l: 40, r: 40 },
        autosize: true,
        height: 700,
        width: 1450,
        legend: { orientation: 'h', y: 1.1, x: 0.5, xanchor: 'center' },
        xaxis: { tickmode: 'array', tickvals: xAxis, ticktext: xAxis, tickangle: 0, automargin: true },
        yaxis: { automargin: true }
      };

      try { Plotly.purge(this.$refs.chart); } catch (e) {}
      Plotly.newPlot(this.$refs.chart, traces, layout, { responsive: true, displayModeBar: false, useResizeHandler: true });
    }
  }
};
</script> 
  