<template>
  <div>
    <el-table
      :data="permissionArr"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
      :expand-row-keys="[]"
    >
      <el-table-column prop="name" label="名称" align="center" />
      <el-table-column prop="code" label="权限值" align="center" />
      <el-table-column prop="level" label="菜单等级" align="center" />
      <el-table-column label="菜单操作" width="400px" align="center">
        <template #="{ row }">
          <el-button
            icon="Plus"
            type="primary"
            size="small"
            @click="addPermission(row)"
          >
            添加菜单
          </el-button>
          <el-button
            type="warning"
            size="small"
            icon="Edit"
            @click="updatePermission(row)"
            :disabled="row.level == 1"
          >
            编辑
          </el-button>
          <el-popconfirm
            :title="`您确定要删除菜单${row.name}吗?`"
            width="250px"
            icon="Delete"
            @confirm="deleteMenu(row.id)"
          >
            <template #reference>
              <el-button
                type="danger"
                size="small"
                icon="Delete"
                :disabled="row.level == 1"
              >
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="dialogFormVisible" width="30%">
      <template #header>
        <span class="header">{{ title }}</span>
        <el-divider></el-divider>
      </template>

      <el-form
        label-width="80px"
        label-position="left"
        :model="menuParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item prop="name">
          <template #label>
            <div class="label">菜单名称</div>
          </template>

          <el-input
            v-model="menuParams.name"
            :placeholder="'请输入菜单名称'"
          ></el-input>
        </el-form-item>
        <el-form-item prop="code">
          <template #label>
            <div class="label">权限值</div>
          </template>

          <el-input
            v-model="menuParams.code"
            :placeholder="'请输入权限值'"
          ></el-input>
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
import {
  reqAllPermission,
  reqAddMenu,
  reqUpdateMenu,
  reqDeleteMenu,
} from '@/api/acl/menu'
import {
  PermissionResponseData,
  PermissionList,
  Permission,
  MenuParams,
} from '@/api/acl/menu/type'

// 控制对话框显示或者隐藏
let dialogFormVisible = ref<boolean>(false)
// 对话框标题
let title = ref<string>('')

// 组件挂载完毕展示数据
onMounted(() => {
  getHasPermission()
})
let permissionArr = ref<PermissionList>([])

const getHasPermission = async () => {
  let result: PermissionResponseData = await reqAllPermission()
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储权限数组
    permissionArr.value = result.data
  }
}

// // 判断有无孩子若没孩子则不可以添加了
// const hasChildren = (value: Permission) => {
//   if (value.children && value.children.length > 0) {
//     return false
//   }
//   return true
// }

let menuParams = reactive<MenuParams>({
  pid: 0,
  code: '',
  level: 0,
  name: '',
})

// 添加菜单按钮
const addPermission = (row: Permission) => {
  // 清空数据
  Object.assign(menuParams, { pid: 0, code: '', level: 0, name: '' })
  title.value = '添加菜单'
  dialogFormVisible.value = true
  // 收集新增数据，由于是网父菜单的子菜单下添加
  menuParams.level = row.level + 1
  menuParams.pid = row.id
}
// 修改菜单按钮
const updatePermission = (row: Permission) => {
  title.value = '修改菜单'
  dialogFormVisible.value = true
  // 收集已有的数据信息
  Object.assign(menuParams, row)
  // clearVali()
}

// 发送请求
const confirm = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  // await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result: any = 1
  if (menuParams.id) {
    result = await reqUpdateMenu(menuParams)
  } else {
    result = await reqAddMenu(menuParams)
  }
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    dialogFormVisible.value = false
    ElMessage({
      type: 'success',
      message: menuParams.id ? '修改菜单成功' : '添加菜单成功',
    })
    // 再次发请求获取全部数据
    getHasPermission()
    // 浏览器自动刷新,更改admin信息后刷新更改右上角用户信息
    setTimeout(() => {
      window.location.reload()
    }, 500)
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: menuParams.id ? '修改菜单失败' : '添加菜单失败',
    })
    dialogFormVisible.value = false
  }
}
// 取消
const cancel = () => {
  // 对话框隐藏
  dialogFormVisible.value = false
}
// 表单校验规则
const rules: Partial<Record<string, any>> = {
  name: [{ required: true, trigger: 'blur' }],
  code: [{ required: true, trigger: 'blur' }],
}

// 删除某一个菜单
const deleteMenu = async (permissionId: number) => {
  let result: any = await reqDeleteMenu(permissionId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    getHasPermission()
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
.header {
  font-size: 30px;
  font-weight: bold;
}
.label {
  font-weight: bold;
}
</style>
