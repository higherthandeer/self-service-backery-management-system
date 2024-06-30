<template>
  <div>
    <el-card style="height: 80px">
      <el-form :inline="true" class="form">
        <el-form-item label="用户名: ">
          <el-input placeholder="请输入搜索用户名" v-model="keyword"></el-input>
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
      <!-- 卡片顶部添加用户按钮 -->
      <el-button type="primary" size="default" icon="Plus" @click="addUser">
        添加用户
      </el-button>
      <el-button
        type="danger"
        size="default"
        icon="Delete"
        :disabled="selectIdArr.length ? false : true"
        @click="deleteBatchUser"
      >
        批量删除
      </el-button>
      <!-- 表格组件展示用户 -->
      <el-table
        @selection-change="selectChange"
        style="margin: 10px 0px"
        border
        :data="userArr"
      >
        <el-table-column type="selection" align="center"></el-table-column>
        <!-- 由于ID是一串复杂数字一般不展示给用户第一列改为序号而不用ID -->
        <el-table-column
          label="序号"
          width="60px"
          align="center"
          type="index"
        ></el-table-column>
        <!-- 循环动态生成表 -->
        <el-table-column
          v-for="column in tableColumnList"
          :prop="column.prop"
          :label="column.label"
          :key="column.prop"
          align="center"
          :width="getColumnWidth(column.prop)"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <!-- 检查列是否为是否过期类型，并显示相应内容 -->
            <template v-if="checkGender(column.prop)">
              <span v-if="row[column.prop] == 1">男</span>
              <span v-else>女</span>
            </template>
            <!-- 如果不是，则显示默认内容 -->
            <template v-else-if="checkRole(column.prop)">
              <span v-for="(item, index) in row[column.prop]" :key="item.id">
                {{ item.name }}
                <!-- 循环展示数据中间用逗号隔开 -->
                <span v-if="index !== row[column.prop].length - 1">,</span>
              </span>
            </template>
            <template v-else>
              {{ row[column.prop] }}
            </template>
          </template>
        </el-table-column>
        <!-- 操作列单独定义 -->
        <el-table-column label="用户操作" width="240px" align="center">
          <template #="{ row }">
            <el-button
              icon="User"
              type="primary"
              size="small"
              @click="setRole(row)"
            >
              分配角色
            </el-button>
            <el-button
              type="warning"
              size="small"
              icon="Edit"
              @click="updateUser(row)"
            ></el-button>
            <el-popconfirm
              :title="`您确定要删除用户${row.username}吗?`"
              width="250px"
              icon="Delete"
              @confirm="deleteUser(row.id)"
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
        @current-change="getHasUser"
        @size-change="sizeChange"
        v-model:current-page="pageNo"
        v-model:page-size="pageLimit"
        :page-sizes="[5, 10, 15, 20]"
        :background="true"
        layout=" prev, pager, next, jumper, ->, total, sizes"
        :total="total"
      />
    </el-card>
    <!-- 抽屉完成添加新的用户| 更新已有账号信息 -->
    <el-drawer v-model="drawer">
      <template #header>
        <h4>{{ title }}</h4>
      </template>
      <template #default>
        <el-form :model="userParams" :rules="rules" ref="formRef">
          <el-form-item label="用户姓名" prop="name">
            <el-input
              placeholder="请输入用户姓名"
              v-model="userParams.name"
            ></el-input>
          </el-form-item>
          <el-form-item label="用户昵称" prop="username">
            <el-input
              placeholder="请输入用户昵称"
              v-model="userParams.username"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="用户密码"
            prop="password"
            v-show="!userParams.id"
          >
            <el-input
              placeholder="请输入用户密码"
              v-model="userParams.password"
            ></el-input>
          </el-form-item>
          <el-button
            v-show="userParams.id"
            type="primary"
            @click="reSetPwd(userParams.id)"
          >
            重置用户密码
          </el-button>
        </el-form>
      </template>
      <template #footer>
        <div style="flex: auto">
          <el-button @click="cancel">取消</el-button>
          <el-button type="primary" @click="confirm">确定</el-button>
        </div>
      </template>
    </el-drawer>
    <!-- 分配角色抽屉 -->
    <el-drawer v-model="drawerRole">
      <template #header>
        <h4>分配角色</h4>
      </template>
      <template #default>
        <el-form>
          <el-form-item label="用户昵称">
            <el-input v-model="userParams.username" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="角色列表">
            <el-checkbox
              v-model="checkAll"
              :indeterminate="isIndeterminate"
              style="margin-right: 100px"
              @change="handleCheckAllChange"
            >
              全 选
            </el-checkbox>
            <el-checkbox-group
              v-model="userRole"
              @change="handleCheckedRolesChange"
            >
              <el-checkbox
                v-for="(role, index) in allRole"
                :key="index"
                :label="role"
              >
                {{ role.name }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <div style="flex: auto">
          <el-button @click="drawerRole = false">取消</el-button>
          <el-button type="primary" @click="confirmRole">确定</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import useLayOutSettingStore from '@/store/modules/setting'
import {
  reqAllUser,
  reqAddUser,
  reqAllRole,
  reqSetUserRole,
  reqDeleteUser,
  reqDeleteBatchUser,
  reqUpdateUser,
  reqResetPwd,
} from '@/api/acl/user'
import {
  UserResponseData,
  Records,
  User,
  AllRoleResponseData,
  SetRoleData,
  AllRole,
} from '@/api/acl/user/type'
// 默认页码
let pageNo = ref<number>(1)
// 一页展示数据条数
let pageLimit = ref<number>(5)
let title = ref<string>('')
// 存储已有商品数据总数
let total = ref<number>(0)
// 存储已有商品数据
let userArr = ref<Records>([])
// 获取商品属性用作表的列属性
let tableColumnList = ref<any>([])
// 控制抽屉显示或者隐藏
let drawer = ref<boolean>(false)
// 控制分配角色抽屉显示或者隐藏
let drawerRole = ref<boolean>(false)
// 全选框
let checkAll = ref<boolean>(false)
// 设置不确定样式
let isIndeterminate = ref<boolean>(true)
// 定义收集新增商品数据
let userParams = reactive<User>({
  username: '',
  name: '',
  password: '',
})
// 获取el-form组件实例
let formRef = ref<any>()
// 目前已有职位
let userRole = ref<AllRole>([])
// 全部职位
let allRole = ref<AllRole>([])
// 组件挂载完毕获取
onMounted(() => {
  getHasUser()
})

// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasUser()
}
// 获取全部用户信息
const getHasUser = async () => {
  let result: UserResponseData = await reqAllUser(
    pageNo.value,
    pageLimit.value,
    keyword.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商品类的总数
    total.value = result.data.total
    userArr.value = result.data.records
    tableColumnList.value = result.data.columns
  }
}

// 判断列是否是性别字段
const checkGender = (value: string) => {
  return value == 'gender'
}
// 判断是否是角色字段
const checkRole = (value: string) => {
  return value == 'role'
}
// 宽度处理
const getColumnWidth = (prop: string) => {
  if (prop == 'gender') {
    // 对性别列的宽度特殊处理
    return '60px'
  } else {
    return 'auto' // 其他列使用自动调整宽度
  }
}
// 添加用户
const addUser = () => {
  // 显示抽屉
  drawer.value = true
  title.value = '添加用户'
  Object.assign(userParams, {
    // id清0防止点击添加按钮弹出编辑窗口
    id: 0,
    username: '',
    name: '',
    password: '',
  })
  clearVali()
}
// 更新用户
const updateUser = (row: User) => {
  drawer.value = true
  title.value = '修改用户'
  // 收集已有的数据信息
  Object.assign(userParams, row)
  clearVali()
}
// 发送请求
const confirm = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result: any = 1
  if (userParams.id) {
    result = await reqUpdateUser(userParams)
  } else {
    result = await reqAddUser(userParams)
  }
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    drawer.value = false
    ElMessage({
      type: 'success',
      message: userParams.id ? '修改用户成功' : '添加用户成功',
    })
    // 再次发请求获取全部数据
    getHasUser()
    // 浏览器自动刷新,更改admin信息后刷新更改右上角用户信息
    window.location.reload()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: userParams.id ? '修改用户失败' : '添加用户失败',
    })
    drawer.value = false
  }
}
// 取消
const cancel = () => {
  // 对话框隐藏
  drawer.value = false
}

// 清空校验信息
const clearVali = () => {
  nextTick(() => {
    formRef.value.clearValidate(['username', 'name', 'password'])
  })
}
// 用户名校验规则
const validatorUsername = (_rule: any, value: any, callback: any) => {
  // 用户昵称长度至少五位
  if (value.trim().length >= 5) {
    callback()
  } else {
    callback(new Error('用户昵称至少五位'))
  }
}
const validatorPassword = (_rule: any, value: any, callback: any) => {
  // 用户昵称长度至少五位
  if (value.trim().length >= 5) {
    callback()
  } else {
    callback(new Error('用户密码至少六位'))
  }
}
// 表单校验规则对象
const rules: Partial<Record<string, any>> = {
  username: [{ required: true, trigger: 'blur', validator: validatorUsername }],
  password: [{ required: true, trigger: 'blur', validator: validatorPassword }],
}
const setRole = async (row: User) => {
  // 存储已有用户信息
  Object.assign(userParams, row)
  // console.log(userParams.id)
  // 存储全部角色信息以及当前角色信息
  let result: AllRoleResponseData = await reqAllRole(userParams.id as number)
  if (result.code == 200) {
    // 存储全部职位
    allRole.value = result.data.allRolesList
    // 存储当前用户已有职位
    userRole.value = result.data.curRoles
    // 显示抽屉
    drawerRole.value = true
  }
  console.log(result)
}
// 全选矿
const handleCheckAllChange = (val: boolean) => {
  userRole.value = val ? allRole.value : []
  isIndeterminate.value = false
}
// 全选勾上全选框
const handleCheckedRolesChange = (value: string[]) => {
  const checkedCount = value.length
  checkAll.value = checkedCount === allRole.value.length
  isIndeterminate.value =
    checkedCount > 0 && checkedCount < allRole.value.length
}
// 发送请求设定角色
const confirmRole = async () => {
  let data: SetRoleData = {
    userId: userParams.id as number,
    // 只需要roleid
    roleIdList: userRole.value.map((item) => {
      return item.id as number
    }),
  }
  console.log(data)
  let result: any = await reqSetUserRole(data)
  if (result.code == 200) {
    // 提示信息
    ElMessage({
      type: 'success',
      message: '分配角色成功',
    })
    // 关闭抽屉
    drawerRole.value = false

    // 获取更新用户信息
    getHasUser()
  } else {
    ElMessage({
      type: 'error',
      message: '分配角色失败',
    })
    drawerRole.value = false
  }
}
// 删除某一个用户
const deleteUser = async (userId: number) => {
  let result: any = await reqDeleteUser(userId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (userArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasUser()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
    })
  }
}
// 批量删除用户id数组
let selectIdArr = ref<User[]>([])
const selectChange = (value: any) => {
  selectIdArr.value = value
}
const deleteBatchUser = async () => {
  // 整理批量删除的参数
  let idList: any = selectIdArr.value.map((item) => {
    return item.id
  })
  // 批量删除请求
  let result: any = await reqDeleteBatchUser(idList)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '批量删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (userArr.value.length <= selectIdArr.value.length) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasUser()
  } else {
    ElMessage({
      type: 'error',
      message: '批量删除失败',
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
  getHasUser()

  // keyword.value = ''
}
// 获取模板setting仓库
let settingStore = useLayOutSettingStore()
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}

const reSetPwd = async (id: number) => {
  let result = await reqResetPwd({ id: id })
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: result.message,
    })
    // 再次发请求获取全部数据
    getHasUser()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: result.message,
    })
    drawer.value = false
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
