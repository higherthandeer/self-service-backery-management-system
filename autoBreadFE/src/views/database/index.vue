<template>
  <div>
    <el-card style="height: 80px">
      <el-form :inline="true" class="form">
        <el-form-item label="备份名: ">
          <el-input
            placeholder="请输入搜索数据备份名"
            v-model="keyword"
          ></el-input>
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
      <el-button type="primary" size="default" icon="Plus" @click="addBackup">
        添加备份
      </el-button>
      <el-button
        type="danger"
        size="default"
        icon="Delete"
        :disabled="selectIdArr.length ? false : true"
        @click="deleteBatchBackup"
      >
        批量删除
      </el-button>
      <!-- 表格组件展示用户 -->
      <el-table
        @selection-change="selectChange"
        style="margin: 10px 0px"
        border
        :data="backupArr"
      >
        <el-table-column type="selection" align="center"></el-table-column>
        <el-table-column
          align="center"
          label="备份ID"
          prop="id"
          width=""
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          align="center"
          label="备份名字"
          prop="backup_name"
          width=""
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          align="center"
          label="备份描述"
          prop="backup_description"
          width=""
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          align="center"
          label="备份时间"
          prop="backup_date"
          width=""
          show-overflow-tooltip
        ></el-table-column>
        <!-- 操作列单独定义 -->
        <el-table-column label="用户操作" width="240px" align="center">
          <template #="{ row }">
            <el-popconfirm
              :title="`您确定要恢复到备份‘${row.backup_name}’吗?`"
              width="250px"
              icon="RefreshRight"
              @confirm="restoreBackup(row.id)"
            >
              <template #reference>
                <el-button type="warning" size="small" icon="RefreshRight">
                  备份恢复
                </el-button>
              </template>
            </el-popconfirm>
            <el-popconfirm
              :title="`您确定要删除备份${row.backup_name}吗?`"
              width="250px"
              icon="Delete"
              @confirm="deleteBackup(row.id)"
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
        @current-change="getHasBackup"
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
        <span class="header">添加备份</span>
        <el-divider></el-divider>
      </template>

      <el-form
        style="width: 80%"
        label-width="100px"
        label-position="left"
        :model="backupParams"
        :rules="rules"
        ref="formRef"
      >
        <el-form-item prop="backupName">
          <template #label>
            <div class="label">备份名</div>
          </template>
          <el-input
            v-model="backupParams.backupName"
            placeholder="请输入备份名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="backupDesc">
          <template #label>
            <div class="label">备份描述</div>
          </template>
          <el-input
            v-model="backupParams.backupDesc"
            placeholder="请输入备份描述"
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
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import useLayOutSettingStore from '@/store/modules/setting'
import {
  reqAllBackup,
  reqAddBackup,
  reqDeleteBackup,
  reqDeleteBatchBackup,
  reqRestoreBackup,
} from '@/api/database'
import { BackupResponseData, Records, Backup } from '@/api/database/type'
// 默认页码
let pageNo = ref<number>(1)
// 一页展示数据条数
let pageLimit = ref<number>(5)
// 存储已有商品数据总数
let total = ref<number>(0)
// 存储已有商品数据
let backupArr = ref<Records>([])
// 控制抽屉显示或者隐藏
let dialogFormVisible = ref<boolean>(false)

// 定义收集新增商品数据
let backupParams = reactive<Backup>({
  backupName: '',
  backupDesc: '',
})
// 获取el-form组件实例
let formRef = ref<any>()
// 目前已有职位
// 组件挂载完毕获取
onMounted(() => {
  getHasBackup()
})

// 分页器每页数据条数发生变化时
const sizeChange = () => {
  // 当前每页数据量发生变化时，页码归一
  pageNo.value = 1
  getHasBackup()
}
// 获取全部用户信息
const getHasBackup = async () => {
  let result: BackupResponseData = await reqAllBackup(
    pageNo.value,
    pageLimit.value,
    keyword.value,
  )
  console.log(result) // 调试用可注释
  if (result.code == 200) {
    // 存储已有商品类的总数
    total.value = result.data.total
    backupArr.value = result.data.records
  }
}
// 添加用户
const addBackup = () => {
  // 显示抽屉
  dialogFormVisible.value = true
  backupParams.backupName = ''
  backupParams.backupDesc = ''
  clearVali()
}
// 发送请求
const confirm = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  await formRef.value.validate()
  let result: any = await reqAddBackup(backupParams)
  console.log(result)
  if (result.code == 200) {
    // 添加成功
    // 对话框隐藏
    dialogFormVisible.value = false
    ElMessage({
      type: 'success',
      message: '添加备份成功',
    })
    // 再次发请求获取全部数据
    getHasBackup()
    // 浏览器自动刷新,更改admin信息后刷新更改右上角用户信息
    window.location.reload()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: backupParams.id ? '修改用户失败' : '添加用户失败',
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
    formRef.value.clearValidate(['username', 'name', 'password'])
  })
}
// 表单校验规则对象
const rules: Partial<Record<string, any>> = {
  backupName: [{ required: true, trigger: 'blur', message: '请输入备份名' }],
}
// 删除某一个用户
const deleteBackup = async (backupId: number) => {
  let result: any = await reqDeleteBackup(backupId)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (backupArr.value.length <= 1) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasBackup()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
    })
  }
}
// 批量删除用户id数组
let selectIdArr = ref<Backup[]>([])
const selectChange = (value: any) => {
  selectIdArr.value = value
}
const deleteBatchBackup = async () => {
  // 整理批量删除的参数
  let idList: any = selectIdArr.value.map((item) => {
    return item.id
  })
  // 批量删除请求
  let result: any = await reqDeleteBatchBackup(idList)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '批量删除成功',
    })
    // 删除成功后再次获取已有的用户数据
    if (backupArr.value.length <= selectIdArr.value.length) {
      //这个lenghth为删除之前的length因此为小于等于1
      pageNo.value -= 1
    }
    getHasBackup()
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
  getHasBackup()

  // keyword.value = ''
}
// 获取模板setting仓库
let settingStore = useLayOutSettingStore()
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}

const restoreBackup = async (rowId: number) => {
  let result = await reqRestoreBackup(rowId)
  console.log(result)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: result.message,
    })
    getHasBackup()
  } else {
    ElMessage({
      type: 'error',
      message: result.message,
    })
  }
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
</style>
