<template>
  <div>
    <!--块类统计-->
    <div class="head">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="middle">
            <h3>库存总数</h3>
            <div class="margin">
              <el-icon color="purple">
                <Goods />
              </el-icon>
              <span style="margin: 0px 5px">{{ invTotal }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>已出库总数</h3>
            <div class="margin">
              <el-icon color="green">
                <SoldOut />
              </el-icon>
              <span style="margin: 0px 5px">{{ outTotal }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>总价值(元)</h3>
            <div class="margin">
              <el-icon color="gold">
                <Money />
              </el-icon>
              <span style="margin: 0px 5px">{{ valueTotal }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>总损失(元)</h3>
            <div class="margin">
              <el-icon color="red"><SortDown /></el-icon>
              <span style="margin: 0px 5px">{{ lossTotal }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <!--echarts统计图-->
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="echarts1">
          <echarts1 />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="echarts2">
          <echarts2 />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, onMounted } from 'vue'
import { reqInventoryHeader } from '@/api/inventory'
import echarts1 from './echarts1/index.vue'
import echarts2 from './echarts2/index.vue'
// import echarts3 from './echarts3/index.vue'

let invTotal = ref<number>(2424132)
let outTotal = ref<number>(12763)
let valueTotal = ref<number>(123)
let lossTotal = ref<number>(28)
let profit = ref<number>(3.58)
let goods = ref([])

// 获取信息
const getHeader = async () => {
  let result: any = await reqInventoryHeader()
  console.log(result)
  if (result.code == 200) {
    invTotal.value = result.data.total_count
    valueTotal.value = result.data.total_value
    outTotal.value = result.data.total_out
    lossTotal.value = result.data.total_loss
  }
}

onMounted(() => {
  getHeader()
})
</script>

<style scoped>
.head {
  margin-bottom: 10px;
  .middle {
    text-align: center;
  }
  .margin {
    margin-top: 10px;
  }
}
.echarts3 {
  height: 555px;
}
.echarts2 {
  height: 510px;
}
</style>
