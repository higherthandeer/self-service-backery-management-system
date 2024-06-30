<template>
  <div>
    <el-card style="height: 80px">
      <el-form :inline="true" class="form">
        <el-form-item label="角色名称: ">
          <el-input placeholder="请输入搜索角色" v-model="keyword"></el-input>
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
      <!-- 卡片顶部添加角色按钮 -->
      <el-button type="primary" size="default" icon="Plus" @click="addRole">
        添加角色
      </el-button>
      <!-- 表格组件展示角色 -->
      <el-table style="margin: 10px 0px" border :data="roleArr">
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
            {{ row[column.prop] }}
          </template>
        </el-table-column>
        <!-- 操作列单独定义 -->
        <el-table-column label="角色操作" width="400px" align="center">
          <template #="{ row }">
            <el-button
              icon="User"
              type="primary"
              size="small"
              @click="setPermission(row)"
            >
              分配权限
            </el-button>
            <el-button
              type="warning"
              size="small"
              icon="Edit"
              @click="updateRole(row)"
            >
              编辑角色
            </el-button>
            <el-popconfirm
              :title="`您确定要删除角色${row.name}吗?`"
              width="250px"
              icon="Delete"
              @confirm="deleteRole(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" icon="Delete">
                  删除角色
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="getHasRole"
        @size-change="sizeChange"
        v-model:current-page="pageNo"
        v-model:page-size="pageLimit"
        :page-sizes="[5, 10, 15, 20]"
        :background="true"
        layout=" prev, pager, next, jumper, ->, total, sizes"
        :total="total"
      />
    </el-card>
    <el-dialog v-model="dialogFormVisible" width="50%">
      <template #header>
        <span class="header">{{ title }}</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 90%"
        label-width="100px"
        label-position="left"
        :model="roleParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item prop="name">
          <template #label>
            <div class="label">角色名称</div>
          </template>

          <el-input
            v-model="roleParams.name"
            :placeholder="'请输入角色名称'"
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
    <el-drawer v-model="drawer">
      <template #header>
        <h4>分配菜单与按钮的权限</h4>
      </template>
      <template #default>
        <!-- 树形控件 -->
        <el-tree
          ref="tree"
          style="max-width: 600px"
          :data="menuArr"
          show-checkbox
          node-key="id"
          default-expanded-all
          :default-checked-keys="selectArr"
          :props="defaultProps"
        />
      </template>
      <template #footer>
        <div style="flex: auto">
          <el-button @click="drawer = false">取消</el-button>
          <el-button type="primary" @click="handerPermission">确定</el-button>
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
  reqAllRole,
  reqAddRole,
  reqUpdateRole,
  reqDeleteRole,
  reqAllMenuList,
  reqSetPermission,
} from '@/api/acl/role'
import {
  RoleResponseData,
  Records,
  Role,
  MenuResponseData,
  MenuList,
} from '@/api/acl/role/type'
// 默认页码
let pageNo = ref<number>(1)
// 一页展示数据条数
let pageLimit = ref<number>(5)
let title = ref<string>('')
// 存储已有角色数据总数
let total = ref<number>(0)
// 存储已有角色数据
let roleArr = ref<Records>([])
// 获取角色属性用作表的列属性
let tableColumnList = ref<any>([])
// 控制抽屉显示或者隐藏
let dialogFormVisible = ref<boolean>(false)
// 设置不确定样式
// let isIndeterminate = ref<boolean>(true)
// 定义收集新增角色数据
let roleParams = reactive<Role>({
  name: '',
})
// 获取el-form组件实例
let formRef = ref<any>()
// 组件挂载完毕获取
onMounted(() => {
  getHasRole()
})

// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasRole()
}
// 获取全部角色信息
const getHasRole = async () => {
  let result: RoleResponseData = await reqAllRole(
    pageNo.value,
    pageLimit.value,
    keyword.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商角色的总数
    total.value = result.data.total
    roleArr.value = result.data.records
    tableColumnList.value = result.data.columns
  }
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
const addRole = () => {
  // 显示抽屉
  dialogFormVisible.value = true
  title.value = '添加角色'
  Object.assign(roleParams, {
    // id清0防止点击添加按钮弹出编辑窗口
    id: 0,
    name: '',
  })
  clearVali()
}
// 更新用户
const updateRole = (row: Role) => {
  dialogFormVisible.value = true
  title.value = '修改角色'
  // 收集已有的数据信息
  Object.assign(roleParams, row)
  clearVali()
}
// 发送请求
const confirm = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  // id用于判断是添加还是修改，如果带有id表明是修改走修改url
  let result: any = 1
  if (roleParams.id) {
    result = await reqUpdateRole(roleParams)
  } else {
    result = await reqAddRole(roleParams)
  }
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    dialogFormVisible.value = false
    ElMessage({
      type: 'success',
      message: roleParams.id ? '修改角色成功' : '添加角色成功',
    })
    // 再次发请求获取全部数据
    getHasRole()
    // 浏览器自动刷新,更改admin信息后刷新更改右上角用户信息
    window.location.reload()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: roleParams.id ? '修改角色失败' : '添加角色失败',
    })
    dialogFormVisible.value = false
  }
}
// 取消
const cancel = () => {
  // 对话框隐藏
  dialogFormVisible.value = false
}

// 清空校验信息
const clearVali = () => {
  nextTick(() => {
    formRef.value.clearValidate(['name'])
  })
}
// 角色名称校验规则
const validatorName = (_rule: any, value: any, callback: any) => {
  // 角色姓名长度至少两位
  if (value.trim().length >= 2) {
    callback()
  } else {
    callback(new Error('角色名称至少两位'))
  }
}
// 表单校验规则对象
const rules: Partial<Record<string, any>> = {
  name: [{ required: true, trigger: 'blur', validator: validatorName }],
}
// const handleCheckAllChange = (val: boolean) => {
//   userRole.value = val ? allRole.value : []
//   isIndeterminate.value = false
// }
// // 全选勾上全选框
// const handleCheckedRolesChange = (value: string[]) => {
//   const checkedCount = value.length
//   checkAll.value = checkedCount === allRole.value.length
//   isIndeterminate.value =
//     checkedCount > 0 && checkedCount < allRole.value.length
// }
// 删除某一个角色
const deleteRole = async (roleId: number) => {
  let result: any = await reqDeleteRole(roleId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (roleArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasRole()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
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
  getHasRole()

  // keyword.value = ''
}
// 获取模板setting仓库
let settingStore = useLayOutSettingStore()
// 重置
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}

// 控制抽屉显示隐藏
let drawer = ref<boolean>(false)
// 定义数组存储权限数据
let menuArr = ref<MenuList>([])
// 数组用于存储勾选的节点的id
let selectArr = ref<number[]>([])
// 定义方法筛选勾选节点id
const filterSelectArr = (allData: any, initArr: any) => {
  allData.forEach((item: any) => {
    if (item.children && item.children.length > 0) {
      filterSelectArr(item.children, initArr)
    } else if (item.select) {
      initArr.push(item.id)
    }
  })
  return initArr
}
// 分配权限
const setPermission = async (row: Role) => {
  drawer.value = true
  // 收集当前要分配权限的职位数据
  Object.assign(roleParams, row)
  // 根据职位获取权限数据
  let result: MenuResponseData = await reqAllMenuList(roleParams.id as number)
  console.log(result)
  if (result.code == 200) {
    menuArr.value = result.data
    selectArr.value = filterSelectArr(menuArr.value, [])
  }
}
let tree = ref<any>()
// 分配权限提交给后端修改
const handerPermission = async () => {
  // roleid
  const roleId = roleParams.id
  // 选中节点的id
  let arr = tree.value.getCheckedKeys()
  //半选的ID
  let arr1 = tree.value.getHalfCheckedKeys()
  let permissionId = arr.concat(arr1)
  // let permissionId = tree.value.getCheckedKeys()
  // console.log(permissionId)
  let result = await reqSetPermission(roleId as number, permissionId)
  if (result.code == 200) {
    // 抽屉关闭
    drawer.value = false
    ElMessage({
      type: 'success',
      message: '分配权限成功',
    })
    // 分配成功页面刷新，若角色权限改变可能显示菜单改变
    // 使用定时器防止直接刷新看不见提示消息
    setTimeout(() => {
      window.location.reload()
    }, 500)
  } else {
    ElMessage({
      type: 'error',
      message: '分配权限失败',
    })
  }
  // console.log(result)
}
const defaultProps = {
  children: 'children',
  label: 'name',
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
