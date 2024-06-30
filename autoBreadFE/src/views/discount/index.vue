<template>
  <div>
    <el-card style="margin: 10px 0px">
      <!-- 添加按钮 -->
      <el-button type="primary" size="default" icon="Plus" @click="addDiscount">
        添加会员折扣
      </el-button>
      <!-- 表格组件展示用户 -->
      <el-table style="margin: 10px 0px" border :data="discountArr">
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
              @click="updateDiscount(row)"
            ></el-button>
            <el-popconfirm
              :title="`您确定要删会员${row.username}吗?`"
              width="250px"
              icon="Delete"
              @confirm="deleteDiscount(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" icon="Delete"></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog v-model="updateFormVisible" width="60%">
      <template #header>
        <span class="header">修改会员等级信息</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 90%"
        label-width="120px"
        label-position="left"
        :model="discountParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item prop="required_score">
          <template #label>
            <div class="label">会员所需积分</div>
          </template>
          <el-input
            v-model="discountParams.required_score"
            placeholder="请输入所需积分"
          ></el-input>
        </el-form-item>
        <el-form-item prop="discount">
          <template #label>
            <div class="label">会员所享折扣</div>
          </template>
          <el-input
            v-model="discountParams.discount"
            placeholder="请输入折扣值"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" size="default" @click="confirmUpdate">
          确定
        </el-button>
        <el-button type="primary" size="default" @click="cancel">
          取消
        </el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="addFormVisible" width="60%">
      <template #header>
        <span class="header">添加会员折扣信息</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 90%"
        label-width="100px"
        label-position="left"
        :model="discountParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item prop="level">
          <template #label>
            <div class="label">会员等级</div>
          </template>
          <el-input
            v-model="discountParams.level"
            placeholder="请输入会员等级"
          ></el-input>
        </el-form-item>
        <el-form-item prop="discount">
          <template #label>
            <div class="label">优惠折扣</div>
          </template>
          <el-input
            v-model="discountParams.discount"
            placeholder="请输入折扣值"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" size="default" @click="confirmAdd">
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
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  reqAllDiscount,
  reqAddDiscount,
  reqUpdateDiscount,
  reqDeleteDiscount,
} from '@/api/discount'
import { DiscountResponseData, Records, Discount } from '@/api/discount/type'
// 默认页码
let pageNo = ref<number>(1)
// 存储已有商品数据总数
// 存储已有商品数据
let discountArr = ref<Records>([])
// 获取商品属性用作表的列属性
let tableColumnList = ref<any>([])
// 控制对话框显示或者隐藏
let updateFormVisible = ref<boolean>(false)
let addFormVisible = ref<boolean>(false)
// 控制分配角色抽屉显示或者隐藏
// 全选框
let discountParams = reactive<Discount>({
  required_score: '',
  discount: '',
})
// 获取el-form组件实例
let formRef = ref<any>()
// 组件挂载完毕获取
onMounted(() => {
  getHasDiscount()
})

// 获取全部用户信息
const getHasDiscount = async () => {
  let result: DiscountResponseData = await reqAllDiscount()
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商品类的总数
    discountArr.value = result.data.records
    tableColumnList.value = result.data.columns
  }
}

const checkLevel = (prop: string) => {
  return prop == 'level' ? true : false
}

let level: any = {
  0: '普通会员',
  1: '一级会员',
  2: '二级会员',
  3: '三级会员',
  4: '四通会员',
  5: '五级会员',
  6: '六级会员',
  7: '七级会员',
  8: '八级会员',
  9: '九级会员',
  10: '十级会员',
}
// 添加用户
const addDiscount = () => {
  // 显示抽屉
  addFormVisible.value = true
  Object.assign(discountParams, {
    // id清0防止点击添加按钮弹出编辑窗口
    id: 0,
    username: '',
    name: '',
    password: '',
  })
  clearVali()
}
// 更新用户
const updateDiscount = (row: Discount) => {
  updateFormVisible.value = true
  // 收集已有的数据信息
  Object.assign(discountParams, row)
  clearVali()
}
// 发送请求
const confirmUpdate = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result = await reqUpdateDiscount(discountParams)
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏

    ElMessage({
      type: 'success',
      message: '修改会员折扣成功',
    })
    // 再次发请求获取全部数据
    getHasDiscount()
  } else {
    ElMessage({
      type: 'error',
      message: '修改会员折扣失败',
    })
  }
  updateFormVisible.value = false
}

// 发送请求
const confirmAdd = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result = await reqAddDiscount(discountParams)
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏

    ElMessage({
      type: 'success',
      message: '添加会员折扣成功',
    })
    // 再次发请求获取全部数据
    getHasDiscount()
  } else {
    ElMessage({
      type: 'error',
      message: '添加会员折扣失败',
    })
  }
  addFormVisible.value = false
}
// 取消
const cancel = () => {
  // 对话框隐藏
  updateFormVisible.value = false
  addFormVisible.value = false
}

// 对价格类型为浮点数自定义校验规则
const validateDiscount = (_rule: any, value: any, callback: any) => {
  const DiscountRegex = /^(10|[0-9])(\.\d{1,2})?$/
  if (!DiscountRegex.test(value)) {
    callback(new Error('请输入正确的折扣信息，10以内且只能包含两位小数'))
  } else {
    callback()
  }
}
// 检查数字
const validateNumber = (_rule: any, value: any, callback: any) => {
  const numberRegex = /^(10|[0-9])$/
  if (!value || !numberRegex.test(value)) {
    callback(new Error('此处需要输入0-10之间的数字'))
  } else {
    callback()
  }
}
// 检查等级
const validateScore = (_rule: any, value: any, callback: any) => {
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
  discount: [
    { required: true, message: '请输入折扣', trigger: 'change' },
    {
      validator: validateDiscount,
      trigger: 'change',
    },
  ],
  level: [
    { required: true, message: '请输入会员等级', trigger: 'change' },
    {
      validator: validateNumber,
      trigger: 'change',
    },
  ],
  required_score: [
    { required: true, message: '请输入所需会员积分', trigger: 'change' },
    {
      validator: validateScore,
      trigger: 'change',
    },
  ],
}

// 清空校验信息
const clearVali = () => {
  nextTick(() => {
    formRef.value.clearValidate(['level', 'discount'])
  })
}

// 删除某一个用户
const deleteDiscount = async (userId: number) => {
  let result: any = await reqDeleteDiscount(userId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (discountArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasDiscount()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
    })
  }
}
</script>

<style scoped>
.form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
