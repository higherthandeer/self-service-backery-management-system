<template>
  <div class="container">
    <el-card class="card">
      <template #header>
        <div class="card-header">
          <h2>修改密码</h2>
        </div>
      </template>
      <el-form :model="originData" ref="originForm">
        <el-form-item v-show="!isChecked">
          <el-input
            type="password"
            v-model="originData.password"
            placeholder="请输入原密码"
            show-password
          ></el-input>
        </el-form-item>
      </el-form>
      <el-form v-show="isChecked" :model="newData" ref="newForm" :rules="rules">
        <el-form-item prop="newPwd">
          <el-input
            type="password"
            v-model="newData.newPwd"
            placeholder="请输入新密码"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item prop="rePwd">
          <el-input
            type="password"
            v-model="newData.rePwd"
            placeholder="请再次输入新密码"
            show-password
          ></el-input>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="footer">
          <el-button class="btn" type="primary" @click="confirm">
            确定
          </el-button>
        </div>
      </template>
    </el-card>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
// 获取用户相关信息库
import useUserStore from '@/store/modules/user'
let UserStore = useUserStore()
// 获取路由对象
let $router = useRouter()
import { reqUpdatePwd } from '@/api/updatePwd'
let isChecked = ref<boolean>(false)
let originData = reactive({
  password: '',
})
let newData = reactive({
  newPwd: '',
  rePwd: '',
})
// 校验密码
const validatorNewPwd = (_rule: any, value: any, callback: any) => {
  const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]+$/
  if (value.length >= 6 && passwordRegex.test(value)) {
    callback()
  } else {
    callback(new Error('密码长度至少6位,且只能存在字母数字和部分符号'))
  }
}
// 二次校验密码
const validatorRePwd = (_rule: any, value: any, callback: any) => {
  if (value == newData.newPwd) {
    callback()
  } else {
    callback(new Error('两次密码输入不一致'))
  }
}
const rules = {
  newPwd: [{ trigger: 'change', validator: validatorNewPwd }],
  rePwd: [{ trigger: 'change', validator: validatorRePwd }],
}

const confirm = async () => {
  let sendParam = {
    isChecked: false,
    data: '',
  }
  if (!isChecked.value) {
    console.log(originData)
    sendParam.isChecked = isChecked.value
    sendParam.data = originData.password
  } else {
    console.log(newData)
    sendParam.isChecked = isChecked.value
    sendParam.data = newData.newPwd
  }
  let result = await reqUpdatePwd(sendParam)
  if (result.code == 200) {
    if (!isChecked.value) {
      // 为原密码验证成功
      isChecked.value = true
      ElMessage({
        type: 'success',
        message: result.message,
      })
    } else {
      // 为修改密码成功
      ElMessage({
        type: 'success',
        message: result.message,
      })
      // 修改密码成功后logout登出
      await UserStore.userLogout()
      // 跳转登陆页面
      $router.replace({ path: '/login' })
    }
  } else {
    ElMessage({
      type: 'error',
      message: result.message,
    })
  }

  console.log(result)
  console.log('确认')
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  .card {
    width: 480px;
  }
  .footer {
    display: flex;
    justify-content: center;
  }
  .btn {
    width: 100%;
  }
}
</style>
