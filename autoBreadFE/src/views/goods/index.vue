<template>
  <div>
    <el-card style="height: 80px">
      <el-form :inline="true" class="form">
        <el-form-item label="商品名: ">
          <el-input placeholder="请输入搜索商品名" v-model="keyword"></el-input>
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
      <!-- 卡片顶部添加商品按钮 -->
      <el-button
        type="primary"
        size="default"
        icon="Plus"
        @click="addGoods"
        v-hasButton="`btn.Goods.add`"
      >
        添加商品
      </el-button>
      <!-- 表格组件展示商品 -->
      <el-table style="margin: 10px 0px" border :data="goodsArr">
        <!-- 由于ID是一串复杂数字一般不展示给用户第一列改为序号而不用ID -->
        <el-table-column
          label="序号"
          width="60px"
          align="center"
          type="index"
        ></el-table-column>
        <!-- 从第二列开始遍历 -->
        <el-table-column
          v-for="column in tableColumnList.slice(1)"
          :prop="column.prop"
          :label="column.label"
          :key="column.prop"
          align="center"
        >
          <template #default="{ row }">
            <!-- 检查列是否为是否过期类型，并显示相应内容 -->
            <!-- <template v-if="checkExpire(column.prop)">
              <span v-if="row[column.prop]">是</span>
              <span v-else>否</span>
            </template> -->
            <!-- 如果不是，则显示默认内容 -->
            <!-- <template v-else>
              {{ row[column.prop] }}
            </template> -->
            <div :style="getCellStyle(row)">
              <!-- 检查列是否为是否过期类型，并显示相应内容 -->
              <span v-if="checkExpire(column.prop) && row[column.prop]">
                是
              </span>
              <span v-else-if="checkExpire(column.prop) && !row[column.prop]">
                否
              </span>
              <span v-else>
                {{ row[column.prop] }}
              </span>
            </div>
          </template>
        </el-table-column>
        <!-- 操作列单独定义 -->
        <el-table-column label="商品操作">
          <template #="{ row }">
            <el-button
              type="warning"
              size="small"
              icon="Edit"
              @click="updateGoods(row)"
            ></el-button>
            <el-popconfirm
              :title="`您确定要删除商品${row.breadname}吗?`"
              width="250px"
              icon="Delete"
              @confirm="removeGoods(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" icon="Delete"></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页器 
      current-page: 设置分页器当前页码
      page-size: 设置每页显示数据条数
      page-sizes: 设置下拉菜单的条数
      backgroung: 设置分页器按钮颜色
      layout: 设置分页器六个子组件布局
    -->
      <el-pagination
        @current-change="getHasGoods"
        @size-change="sizeChange"
        :pager-count="9"
        v-model:current-page="pageNo"
        v-model:page-size="pageLimit"
        :page-sizes="[5, 10, 15, 20]"
        :background="true"
        layout=" prev, pager, next, jumper, ->, total, sizes"
        :total="total"
      />
    </el-card>
    <!-- 对话框： 添加与编辑 -->
    <!-- v-model控制对话框显示或者隐藏 -->
    <el-dialog v-model="dialogFormVisible" width="60%">
      <template #header>
        <span class="header">{{ title }}</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 90%"
        label-width="100px"
        label-position="left"
        :model="goodsParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item
          v-for="(column, index) in tableColumnList.slice(1)"
          :prop="column.prop"
          :key="index"
        >
          <template #label>
            <div class="label">{{ column.label }}</div>
          </template>
          <template v-if="typeof goodsParams[column.prop] === 'boolean'">
            <el-radio-group v-model="goodsParams[column.prop]">
              <el-radio :label="true" border>是</el-radio>
              <el-radio :label="false" border>否</el-radio>
            </el-radio-group>
          </template>
          <!-- 如果是日期属性显示日期框 -->
          <template v-else-if="column.prop === 'MFG_date'">
            <el-date-picker
              v-model="goodsParams[column.prop]"
              type="date"
              placeholder="选择日期时间"
              value-format="YYYY-MM-DD"
            ></el-date-picker>
          </template>
          <template v-else>
            <el-input
              v-model="goodsParams[column.prop]"
              :placeholder="'请输入' + column.label"
            ></el-input>
          </template>
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
import { ElMessage } from 'element-plus'
import { ref, reactive, onMounted, nextTick } from 'vue'
import {
  reqHasGoods,
  reqAddGoods,
  reqUpdateGoods,
  reqDeleteGoods,
  reqExpireGoods,
} from '@/api/goods'
import type { Records, GoodsResponseData, Goods } from '@/api/goods/type'
import useLayOutSettingStore from '@/store/modules/setting'
// 定义一个title给dialog区分是添加还是修改商品
let title = ref<string>('')
let pageNo = ref<number>(1)
let pageLimit = ref<number>(5)
// 存储已有商品数据总数
let total = ref<number>(0)
// 存储已有商品数据
let goodsArr = ref<Records>([])
// 获取商品属性用作表的列属性
let tableColumnList = ref<any>([])
// 控制对话框显示或者隐藏
let dialogFormVisible = ref<boolean>(false)
// 获取el-form组件实例
let formRef = ref()
// 定义收集新增商品数据
let goodsParams = reactive<Goods>({
  breadname: '',
  price: 0,
  MFG_date: '',
  shield_life: 0,
  count: 0,
  sale_count: 0,
  is_expired: false,
})
// 获取商品接口封装为一个函数
const getHasGoods = async () => {
  let result: GoodsResponseData = await reqHasGoods(
    pageNo.value,
    pageLimit.value,
    keyword.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商品类的总数
    total.value = result.data.total
    goodsArr.value = result.data.records
    tableColumnList.value = result.data.columns
  }
}
const checkExpire = (value: string) => {
  return value == 'is_expired'
}
const getCellStyle = (row: any) => {
  // 如果列是is_expired且值为是，返回红色字体样式
  if (row['is_expired']) {
    return {
      color: 'red',
    }
  }
}
// 判断列是否是过期字段

// 组件挂载完毕则发请求
onMounted(() => {
  getHasGoods()
  getExpireGoods()
})

// // 分页器页码发生变化出发
// const changePageNo = () => {
//   // 页码发生变化再次发送请求获取已有商品数据
//   getHasGoods()
// }

// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasGoods()
}

// 添加商品
const addGoods = () => {
  title.value = '添加商品'
  // id置0防止先点修改再点添加的情况下由于出现id而走了错误接口
  goodsParams.id = 0
  // 添加数据前先清空
  goodsParams.breadname = ''
  goodsParams.price = 0
  goodsParams.MFG_date = ''
  goodsParams.sheld_life = 0
  goodsParams.count = 0
  goodsParams.sale_count = 0
  goodsParams.is_expired = false
  // 显示对话框
  dialogFormVisible.value = true
  // 点击添加按钮清空校验
  clearVali()
}
// 修改商品
const updateGoods = (row: Goods) => {
  // console.log(row)
  title.value = '修改商品'
  dialogFormVisible.value = true
  goodsParams.id = row.id
  // 循环展示已有品牌数据
  // for (const column of tableColumnList.value.slice(1)) {
  //   const key = column.prop
  //   goodsParams[key] = row[key]
  // }
  // ES6语法合并对象
  Object.assign(goodsParams, row)
  clearVali()
}
// 对话框底部取消按钮
const cancel = () => {
  // 对话框隐藏
  dialogFormVisible.value = false
}
// 确定
const confirm = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result: any = 1
  if (goodsParams.id) {
    result = await reqUpdateGoods(goodsParams)
  } else {
    result = await reqAddGoods(goodsParams)
  }
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    dialogFormVisible.value = false
    ElMessage({
      type: 'success',
      message: goodsParams.id ? '修改商品成功' : '添加商品成功',
    })
    // 再次发请求获取全部数据
    getHasGoods()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: goodsParams.id ? '修改商品失败' : '添加商品失败',
    })
    dialogFormVisible.value = false
  }
}
// 清空校验信息
const clearVali = () => {
  nextTick(() => {
    formRef.value.clearValidate([
      'breadname',
      'price',
      'MFG_date',
      'shield_life',
      'count',
      'sale_count',
      'is_expired',
    ])
  })
}

// 对价格类型为浮点数自定义校验规则
const validatePrice = (_rule: any, value: any, callback: any) => {
  const priceRegex = /^\d+(\.\d{1,2})?$/
  if (!priceRegex.test(value)) {
    callback(new Error('请输入正确的价格，最多保留两位小数'))
  } else {
    callback()
  }
}
// 检查数字
const validateNumber = (_rule: any, value: any, callback: any) => {
  const numberRegex = /^\d+$/
  if (!value || !numberRegex.test(value)) {
    callback(new Error('此处需要输入非负整数'))
  } else {
    callback()
  }
}
// 表单校验规则对象
const rules: Partial<Record<string, any>> = {
  // required表明是必须字段，trigger:校验时机blur:失去焦点,change:文本变化
  breadname: [{ required: true, trigger: 'blur', message: '请输入面包名称' }],
  price: [
    { required: true, message: '请输入单价', trigger: 'blur' },
    {
      validator: validatePrice,
      trigger: 'blur',
    },
  ],
  MFG_date: [{ required: true, message: '请输入生产日期', trigger: 'blur' }],
  shield_life: [
    { required: true, message: '请输入保质期(天)', trigger: 'blur' },
    { validator: validateNumber, trigger: 'blur' },
  ],
  count: [
    { required: true, message: '请输入商品总数', trigger: 'blur' },
    { validator: validateNumber, trigger: 'blur' },
  ],
  sale_count: [
    { required: true, message: '请输入售出数量', trigger: 'blur' },
    { validator: validateNumber, trigger: 'blur' },
  ],
  is_expired: [{ required: true, message: '请选择是否过期', trigger: 'blur' }],
}

// 气泡确认删除
const removeGoods = async (id: number) => {
  // 点击确定按钮删除已有商品
  let result = await reqDeleteGoods(id)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除商品成功',
    })
    // 删除成功后再次获取已有的品牌数据
    if (goodsArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasGoods()
  } else {
    ElMessage({
      type: 'error',
      message: '删除商品失败',
    })
  }
}

const getExpireGoods = async () => {
  let result = await reqExpireGoods()
  console.log(result)
  if (result.code == 200) {
    ElMessage({
      type: 'warning',
      message: result.message,
    })
  }
}
// 定义响应式收集用户输入进来的关键字
let keyword = ref<string>('')
// 搜索函数
const search = () => {
  // 为防止搜索后当前页数大于搜索所得所有数据页数报错，返回第一页
  pageNo.value = 1
  // 根据关键字获取响应数据
  getHasGoods()

  // keyword.value = ''
}
// 获取模板setting仓库
let settingStore = useLayOutSettingStore()
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}
</script>

<style scoped>
.header {
  font-size: 30px;
  font-weight: bold;
}
.label {
  font-weight: bold;
}
.form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
