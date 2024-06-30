<template>
  <div class="register_container">
    <el-row>
      <el-col :span="8" :xs="0"></el-col>
      <el-col :span="12" :xs="24">
        <el-form
          class="register_form"
          :model="registerInfo"
          :rules="rules"
          ref="registerForm"
        >
          <h1>Hello</h1>
          <h2>欢迎来到注册页面</h2>
          <el-form-item prop="username">
            <el-input
              placeholder="请输入用户名"
              :prefix-icon="User"
              v-model="registerInfo.username"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              placeholder="请输入密码"
              :prefix-icon="Lock"
              type="password"
              v-model="registerInfo.password"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item prop="repassword">
            <el-input
              placeholder="请再次输入密码"
              :prefix-icon="Lock"
              type="password"
              v-model="registerInfo.repassword"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="btn" type="primary" @click="register">
              注册
            </el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup name="">
import { User, Lock } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'

import { reqRegister } from '@/api/user'
import { registerResponseData } from '@/api/user/type'

// 获取el-form组件
let registerForm = ref()
// 获取路由器
let $router = useRouter()
// 收集账号与密码
let registerInfo = reactive({
  username: '',
  password: '',
  repassword: '',
})
// 校验用户名
const validatorUserName = (_rule: any, value: any, callback: any) => {
  // rule：即为校验规则对象, value: 即为表单元素文本内容, 函数：如果符合条件callback放行通过，不符合则注入错误提示信息
  const usernameRegex = /^[A-Za-z0-9]{5,}$/
  if (usernameRegex.test(value)) {
    callback()
  } else {
    callback(new Error('用户名只能由字母和数字组成且不能少于5位！'))
  }
}
// 校验密码
// 校验密码
const validatorPwd = (_rule: any, value: any, callback: any) => {
  const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]+$/
  if (value.length >= 6 && passwordRegex.test(value)) {
    callback()
  } else {
    callback(new Error('密码长度至少6位,且只能存在字母数字和部分符号'))
  }
}
// 二次校验密码
const validatorRePwd = (_rule: any, value: any, callback: any) => {
  if (value == registerInfo.password) {
    callback()
  } else {
    callback(new Error('两次密码输入不一致'))
  }
}
// 定义表单校验需要配置对象
const rules = {
  username: [
    // { required: true, message: '账号长度至少为6位', rigger: 'change', min: 6, max: 10,},
    { trigger: 'change', validator: validatorUserName },
  ],
  password: [{ trigger: 'change', validator: validatorPwd }],
  repassword: [{ trigger: 'change', validator: validatorRePwd }],
}
const register = async () => {
  // 保证全部表单校验通过在发请求
  await registerForm.value.validate()
  let result: registerResponseData = await reqRegister(registerInfo)
  console.log(result)
  if (result.code == 200) {
    ElNotification({
      type: 'success',
      message: '注册成功',
    })
    $router.push('/login')
  } else {
    ElNotification({
      type: 'error',
      message: result.message,
    })
  }
}
</script>

<style scoped>
.register_container {
  width: 100%;
  height: 100vh;
  /* background-color: rgb(162, 169, 173); */
  background: url('@/assets/images/donuts.png') no-repeat;
  background-size: cover;
  padding: none;
}
.register_form {
  width: 70%;
  margin-top: 20vh;
  background: url('@/assets/images/login_form.png');
  padding: 40px;
  h1 {
    color: white;
  }
  h2 {
    color: white;
    margin: 20px 0;
  }
  .btn {
    width: 100%;
    margin-top: 10px;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
