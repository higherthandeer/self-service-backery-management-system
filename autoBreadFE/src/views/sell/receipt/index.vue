<template>
  <div>
    <el-card>
      <el-table :data="receiptArr" border style="width: 100%">
        <el-table-column type="expand">
          <template #default="props">
            <div>
              <h3 class="receipt-title">销售单具体明细</h3>
              <el-table :data="props.row.detail" border>
                <el-table-column label="#" width="50px" />
                <el-table-column label="名称" prop="breadname" />
                <el-table-column label="单价" prop="price" />
                <el-table-column label="数量" prop="quantity" />
                <el-table-column label="部分总计" prop="sub_total" />
              </el-table>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="ID" prop="id" />
        <el-table-column label="总计" prop="total" />
        <el-table-column label="时间" prop="date" />
        <el-table-column label="会员ID">
          <template #="{ row }">
            <span v-if="row.customer_id == null">匿名会员</span>
            {{ row.customer_id }}
          </template>
        </el-table-column>
        <el-table-column label="会员享受折扣" prop="discount" />
      </el-table>
      <!-- 分页器 
      current-page: 设置分页器当前页码
      page-size: 设置每页显示数据条数
      page-sizes: 设置下拉菜单的条数
      backgroung: 设置分页器按钮颜色
      layout: 设置分页器六个子组件布局
    -->
      <div class="pagnation">
        <el-pagination
          @current-change="getHasReceipt"
          @size-change="sizeChange"
          :pager-count="9"
          v-model:current-page="pageNo"
          v-model:page-size="pageLimit"
          :page-sizes="[5, 10, 15, 20]"
          :background="true"
          layout=" prev, pager, next, jumper, ->, total, sizes"
          :total="total"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, onMounted } from 'vue'
import { reqAllReceipt } from '@/api/sell/receipt'
import { ReceiptResponseData, Records } from '@/api/sell/receipt/type'

let pageNo = ref<number>(1)
let pageLimit = ref<number>(5)
let receiptArr = ref<Records>([])
// 存储已有商品数据总数
let total = ref<number>(0)

const getHasReceipt = async () => {
  let result: ReceiptResponseData = await reqAllReceipt(
    pageNo.value,
    pageLimit.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有订单类的总数
    total.value = result.data.total
    receiptArr.value = result.data.records
  }
}
// 组件挂载完毕则发请求
onMounted(() => {
  getHasReceipt()
})

// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasReceipt()
}
</script>

<style scoped>
.form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header {
  font-size: 30px;
  font-weight: bold;
}
.label {
  font-weight: bold;
}
.pagnation {
  margin-top: 10px;
}
.receipt-title {
  padding: 10px;
}
</style>
