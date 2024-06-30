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
    data: ['各类库存价值', '各类库存损失'],
  },
  radar: {
    // shape: 'circle',
    indicator: [
      { name: '千层蛋糕', max: 6500 },
      { name: '甜甜圈', max: 16000 },
      { name: '法棍', max: 30000 },
      { name: '牛角包', max: 38000 },
      { name: '三明治', max: 52000 },
    ],
  },
  series: [
    {
      name: 'Budget vs spending',
      type: 'radar',
      data: [
        {
          value: [4200, 3000, 20000, 35000, 50000, 18000],
          name: '各类库存损失',
        },
        {
          value: [5000, 14000, 28000, 26000, 42000, 21000],
          name: '各类库存价值',
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
