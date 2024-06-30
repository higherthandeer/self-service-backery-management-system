<template>
  <div ref="echarts3" class="echarts3"></div>
</template>

<script lang="ts" setup name="echarts1">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

let echarts3 = ref()

// mycharts的配置项

const options = {
  legend: {
    data: ['Allocated Budget', 'Actual Spending'],
  },
  radar: {
    // shape: 'circle',
    indicator: [
      { name: 'Sales', max: 6500 },
      { name: 'Administration', max: 16000 },
      { name: 'Information Technology', max: 30000 },
      { name: 'Customer Support', max: 38000 },
      { name: 'Development', max: 52000 },
      { name: 'Marketing', max: 25000 },
    ],
  },
  series: [
    {
      name: 'Budget vs spending',
      type: 'radar',
      data: [
        {
          value: [4200, 3000, 20000, 35000, 50000, 18000],
          name: 'Allocated Budget',
        },
        {
          value: [5000, 14000, 28000, 26000, 42000, 21000],
          name: 'Actual Spending',
        },
      ],
    },
  ],
}

onMounted(() => {
  let mycharts = echarts.init(echarts3.value)
  mycharts.setOption(options)
})
</script>

<style scoped>
.echarts3 {
  width: auto;
  height: 185px;
}
</style>
