<template>
  <div class="curve">
    <div class="select">
      <el-select
        v-model="axisX"
        placeholder="请选择统计单位/年/月/日"
        size="small"
        style="width: 240px"
      >
        <el-option
          v-for="item in selectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>
    <div class="date-picker">
      <el-form-item>
        <el-date-picker
          v-model="date"
          :type="type"
          placeholder="请选择日期"
          size="small"
          :disabled="isDisabled"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
    </div>
    <div class="btn">
      <el-button size="small" @click="confirm">确定</el-button>
    </div>
  </div>
  <div ref="echarts1" class="echarts1"></div>
</template>

<script lang="ts" setup name="echarts1">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import {
  reqSellPerYear,
  reqSellPerMonth,
  reqSellPerDay,
} from '@/api/sell/detail'
let axisX = ref('')
let date = ref('')
let isDisabled = ref(false)
let type = ref('')

const selectOptions = [
  {
    value: 'year',
    label: '年',
  },
  {
    value: 'month',
    label: '月',
  },
  {
    value: 'day',
    label: '日',
  },
]

watch(
  axisX,
  (newValue, _oldValue) => {
    // 当axisX的值变化时，这个函数会被调用
    if (newValue == 'year') {
      isDisabled.value = true
    } else if (newValue == 'month') {
      type.value = 'year'
      isDisabled.value = false
    } else if (newValue == 'day') {
      type.value = 'month'
      isDisabled.value = false
    }
    // 如果有需要，你也可以处理其他值的情况
  },
  {
    immediate: true,
  },
)

const getDate = (dateString: string) => {
  const [yearStr, monthStr, dayStr] = dateString.split('-')
  return { year: yearStr, month: monthStr, day: dayStr }
}

let returnData: any = ref([])
let newData: any = ref([])

const getSellPerDay = async () => {
  let year = getDate(date.value).year
  let month = getDate(date.value).month
  let result = await reqSellPerDay(year, month)
  if (result.code == 200) {
    // console.log(result)
    returnData.value = result.data
    newData.value = returnData.value.map((item: any) => ({
      x: item.day, // 将 year 属性的值赋给新的 x 属性
      total: item.total,
    }))
    drawChart() // 数据加载完成后绘制图表
  }
}
const getSellPerMonth = async () => {
  let year = getDate(date.value).year
  let result = await reqSellPerMonth(year)
  if (result.code == 200) {
    returnData.value = result.data
    newData.value = returnData.value.map((item: any) => ({
      x: item.month, // 将 year 属性的值赋给新的 x 属性
      total: item.total,
    }))
    drawChart() // 数据加载完成后绘制图表
  }
}

const getSellPerYear = async () => {
  let result = await reqSellPerYear()
  if (result.code == 200) {
    // console.log(result)
    returnData.value = result.data
    newData.value = returnData.value.map((item: any) => ({
      x: item.year, // 将 year 属性的值赋给新的 x 属性
      total: item.total,
    }))

    drawChart() // 数据加载完成后绘制图表
  }
}

// mycharts的配置项
let echarts1 = ref()
const colors = ['#5470C6', '#EE6666']
let mycharts: any = null
const drawChart = () => {
  // 确保echarts1.value是一个DOM元素
  if (echarts1.value && newData.value) {
    if (!mycharts) {
      // 如果还没有 ECharts 实例，则创建一个
      mycharts = echarts.init(echarts1.value)
    }
    const options = {
      title: { text: '销售统计图' },
      color: colors,
      tooltip: {
        trigger: 'axis', // 可以改为'axis'来在轴上显示提示
        axisPointer: {
          type: 'cross',
        },
      },
      legend: {},
      grid: {
        top: 70,
        bottom: 50,
      },
      xAxis: {
        type: 'category',
        data: newData.value.map((item: any) => item.x),
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          data: returnData.value.map((item: any) => item.total),
          type: 'line',
          smooth: true,
          emphasis: {
            focus: 'series',
          },
        },
      ],
    }
    mycharts.setOption(options)
  }
}

const confirm = () => {
  console.log(axisX.value)
  console.log(date.value)
  if (axisX.value == 'month' && date.value) {
    getSellPerMonth()
  } else if (axisX.value == 'day' && date.value) {
    getSellPerDay()
  } else {
    getSellPerYear()
  }
}

onMounted(() => {
  getSellPerYear()
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
