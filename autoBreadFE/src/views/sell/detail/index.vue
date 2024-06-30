<template>
  <div>
    <!--块类统计-->
    <div class="head">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="middle">
            <h3>商品销量</h3>
            <div class="margin">
              <el-icon color="purple">
                <shop />
              </el-icon>
              <span style="margin: 0px 5px">{{ saleCounts }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>累计用户数</h3>
            <div class="margin">
              <el-icon color="green">
                <UserFilled />
              </el-icon>
              <span style="margin: 0px 5px">{{ userCounts }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>月盈利增长率</h3>
            <div class="margin">
              <el-icon color="red">
                <TopRight />
              </el-icon>
              <span style="margin: 0px 5px">{{ increase }}%</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="middle">
            <h3>总收入(元)</h3>
            <div class="margin">
              <el-icon color="gold"><WalletFilled /></el-icon>
              <span style="margin: 0px 5px">{{ profit }}</span>
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
import { reqHeader } from '@/api/sell/detail'
import echarts1 from './echarts1/index.vue'
import echarts2 from './echarts2/index.vue'
// import echarts3 from './echarts3/index.vue'

let saleCounts = ref<number>(2424132)
let userCounts = ref<number>(12763)
let increase = ref<number>(28)
let profit = ref<number>(3.58)
let goods = ref([])

// 获取信息
const getHeader = async () => {
  let result = await reqHeader()
  console.log(result)
  if (result.code == 200) {
    saleCounts.value = result.data.saleCounts
    userCounts.value = result.data.userCounts
    profit.value = result.data.profit
    goods.value = result.data.goods
    increase.value = result.data.growth_rate
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
  margin-top: 10px;
}
.echarts2 {
  height: 555px;
}
</style>
