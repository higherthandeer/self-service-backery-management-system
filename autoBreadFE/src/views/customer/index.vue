<template>
  <div>
    <el-card style="height: 80px">
      <el-form :inline="true" class="form">
        <el-form-item label="会员ID: ">
          <el-input placeholder="请输入搜索会员ID" v-model="keyword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="default"
            @click="search"
            :disabled="keyword ? false : true"
          >
            搜索
          </el-button>
          <el-button type="primary" size="default" @click="reset">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card style="margin: 10px 0px">
      <!-- 表格组件展示用户 -->
      <el-table style="margin: 10px 0px" border :data="customerArr">
        <!-- 由于ID是一串复杂数字一般不展示给用户第一列改为序号而不用ID -->

        <!-- 循环动态生成表 -->
        <el-table-column
          v-for="column in tableColumnList"
          :prop="column.prop"
          :label="column.label"
          :key="column.prop"
          align="center"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <template v-if="checkLevel(column.prop)">
              <span>{{ level[row[column.prop]] }}</span>
            </template>
            <template v-else>
              {{ row[column.prop] }}
            </template>
          </template>
        </el-table-column>
        <!-- 操作列单独定义 -->
        <el-table-column label="会员操作" width="240px" align="center">
          <template #="{ row }">
            <el-button
              type="warning"
              size="small"
              icon="Edit"
              @click="updateCustomer(row)"
            ></el-button>
            <el-popconfirm
              :title="`您确定要删会员${row.username}吗?`"
              width="250px"
              icon="Delete"
              @confirm="deleteCustomer(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" icon="Delete"></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页器 -->
      <el-pagination
        @current-change="getHasCustomer"
        @size-change="sizeChange"
        v-model:current-page="pageNo"
        v-model:page-size="pageLimit"
        :page-sizes="[5, 10, 15, 20]"
        :background="true"
        layout=" prev, pager, next, jumper, ->, total, sizes"
        :total="total"
      />
    </el-card>
    <el-dialog v-model="dialogFormVisible" width="60%">
      <template #header>
        <span class="header">修改会员等级</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 90%"
        label-width="100px"
        label-position="left"
        :model="customerParams"
      >
        <el-form-item>
          <el-radio-group v-model="customerParams.level">
            <el-radio :label="0">普通会员</el-radio>
            <el-radio :label="1">一级会员</el-radio>
            <el-radio :label="2">二级会员</el-radio>
            <el-radio :label="3">三级会员</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" size="default" @click="confirm">
          确定
        </el-button>
        <el-button type="primary" size="default" @click="cancel">
          取消
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import useLayOutSettingStore from '@/store/modules/setting'
import {
  reqAllCustomer,
  reqUpdateCustomer,
  reqDeleteCustomer,
} from '@/api/customer'
import { CustomerResponseData, Records, Customer } from '@/api/customer/type'
// 默认页码
let pageNo = ref<number>(1)
// 一页展示数据条数
let pageLimit = ref<number>(5)
// 存储已有商品数据总数
let total = ref<number>(0)
// 存储已有商品数据
let customerArr = ref<Records>([])
// 获取商品属性用作表的列属性
let tableColumnList = ref<any>([])
// 控制对话框显示或者隐藏
let dialogFormVisible = ref<boolean>(false)
// 修改会员等级参数
let customerParams = reactive<Customer>({
  id: 0,
  level: 0,
})
// 组件挂载完毕获取
onMounted(() => {
  getHasCustomer()
})

const checkLevel = (prop: string) => {
  return prop == 'level' ? true : false
}

let level: any = {
  0: '普通会员',
  1: '一级会员',
  2: '二级会员',
  3: '三级会员',
}
// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasCustomer()
}

// 定义响应式收集用户输入进来的关键字
let keyword = ref<any>('')
// 获取全部用户信息
const getHasCustomer = async () => {
  let result: CustomerResponseData = await reqAllCustomer(
    pageNo.value,
    pageLimit.value,
    keyword.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商品类的总数
    total.value = result.data.total
    customerArr.value = result.data.records
    tableColumnList.value = result.data.columns
    ElMessage({
      type: 'success',
      message: '获取成功',
    })
  } else {
    ElMessage({
      type: 'error',
      message: result.message,
    })
  }
}

// 更新用户
const updateCustomer = (row: any) => {
  dialogFormVisible.value = true
  // 收集已有的数据信息
  customerParams.id = row.id
}
// 发送请求
const confirm = async () => {
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result = await reqUpdateCustomer(customerParams)
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    dialogFormVisible.value = false
    ElMessage({
      type: 'success',
      message: '修改用户等级成功',
    })
    // 再次发请求获取全部数据
    getHasCustomer()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: '修改用户等级失败',
    })
    dialogFormVisible.value = false
  }
}
// 取消
const cancel = () => {
  // 对话框隐藏
  dialogFormVisible.value = false
}

// 删除某一个用户
const deleteCustomer = async (customerId: number) => {
  let result: any = await reqDeleteCustomer(customerId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (customerArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasCustomer()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
    })
  }
}

// 搜索函数
const search = () => {
  // 为防止搜索后当前页数大于搜索所得所有数据页数报错，返回第一页
  pageNo.value = 1
  // 根据关键字获取响应数据

  getHasCustomer()
}
// 获取模板setting仓库
let settingStore = useLayOutSettingStore()
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}
</script>

<style scoped>
.form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
