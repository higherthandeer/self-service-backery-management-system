<template>
  <div ref="echarts1" class="echarts1"></div>
</template>

<script lang="ts" setup name="echarts1">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { reqInventoryValueCate } from '@/api/inventory'

let valueData: any = ref([])
let lossData: any = ref([])
let newData: any = ref([])

const getValueCate = async () => {
  let result: any = await reqInventoryValueCate()
  console.log(result)
  if (result.code == 200) {
    // console.log(result)
    valueData.value = result.data.value
    lossData.value = result.data.loss
    // console.log(valueData.value)
    // newData.value = valueData.value.map((item: any) => ({
    //   x: item.year, // 将 year 属性的值赋给新的 x 属性
    //   total: item.total,
    // }))
    drawChart() // 数据加载完成后绘制图表
  }
}

// mycharts的配置项
let echarts1 = ref()
let mycharts: any = null
const drawChart = () => {
  // 确保echarts1.value是一个DOM元素
  if (echarts1.value && newData.value) {
    if (!mycharts) {
      // 如果还没有 ECharts 实例，则创建一个
      mycharts = echarts.init(echarts1.value)
    }
    // const options = {
    //   title: { text: '销售统计图' },
    //   color: colors,
    //   tooltip: {
    //     trigger: 'axis', // 可以改为'axis'来在轴上显示提示
    //     axisPointer: {
    //       type: 'cross',
    //     },
    //   },
    //   legend: {},
    //   grid: {
    //     top: 70,
    //     bottom: 50,
    //   },
    //   xAxis: {
    //     type: 'category',
    //     data: newData.value.map((item: any) => item.x),
    //   },
    //   yAxis: {
    //     type: 'value',
    //   },
    //   series: [
    //     {
    //       data: returnData.value.map((item: any) => item.total),
    //       type: 'line',
    //       smooth: true,
    //       emphasis: {
    //         focus: 'series',
    //       },
    //     },
    //   ],
    // }
    const options = {
      title: {
        text: '各类商品总价值与损失',
      },
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        data: ['总价值', '总损失'],
      },
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: false },
          magicType: { show: true, type: ['line', 'bar'] },
          restore: { show: true },
          saveAsImage: { show: true },
        },
      },
      calculable: true,
      xAxis: [
        {
          type: 'category',
          // prettier-ignore
          data: valueData.value.map((item: any) => item.breadname),
        },
      ],
      yAxis: [
        {
          type: 'value',
        },
      ],
      series: [
        {
          name: '总价值',
          type: 'bar',
          data: valueData.value.map((item: any) => item.value),
          itemStyle: {
            color: '#95d475',
          },

          // markPoint: {
          //   data: [
          //     { type: 'max', name: 'Max' },
          //     { type: 'min', name: 'Min' },
          //   ],
          // },
          // markLine: {
          //   data: [{ type: 'average', name: 'Avg' }],
          // },
        },
        {
          name: '总损失',
          type: 'bar',
          data: lossData.value.map((item: any) => item.loss),
          itemStyle: {
            color: '#f56c6c', // 例如，设置为红色
          },
          // markPoint: {
          //   data: [
          //     { name: 'Max', value: 182.2, xAxis: 7, yAxis: 183 },
          //     { name: 'Min', value: 2.3, xAxis: 11, yAxis: 3 },
          //   ],
          // },
          // markLine: {
          //   data: [{ type: 'average', name: 'Avg' }],
          // },
        },
      ],
    }
    mycharts.setOption(options)
  }
}

onMounted(() => {
  getValueCate()
})
onBeforeUnmount(() => {
  if (mycharts) {
    mycharts.dispose() // 销毁 ECharts 实例
    mycharts = null // 清空引用
  }
})
</script>

<style scoped>
.curve {
  display: flex;
  .date-picker {
    margin-left: 200px;
  }
  .btn {
    margin-left: 30px;
  }
}
.echarts1 {
  width: auto;
  height: 470px;
}
.date-picker {
  margin-left: 30px;
}
</style>
