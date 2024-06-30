<template>
  <div ref="echarts2" class="echarts2"></div>
</template>

<script lang="ts" setup name="echarts1">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reqCatagory } from '@/api/sell/detail'

let echarts2 = ref()
let mycharts: any = null
let returnData: any = ref([])
// newData.value.map((item: any) => item.x),
// mycharts的配置项

const drawChart = () => {
  // 确保echarts1.value是一个DOM元素
  if (echarts2.value && returnData.value) {
    if (!mycharts) {
      // 如果还没有 ECharts 实例，则创建一个
      mycharts = echarts.init(echarts2.value)
    }
    const options = {
      title: {
        text: '各类商品盈利额',
        left: 'center',
      },
      tooltip: {
        trigger: 'item',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
      },
      series: [
        {
          name: 'Access From',
          type: 'pie',
          radius: '50%',
          data: returnData.value,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    }
    mycharts.setOption(options)
  }
}

const getCatagory = async () => {
  let result = await reqCatagory()
  if (result.code == 200) {
    returnData.value = result.data
    drawChart()
  }
  console.log(result)
}

onMounted(() => {
  getCatagory()
})
</script>

<style scoped>
.echarts2 {
  width: auto;
  height: 225px;
}
</style>
