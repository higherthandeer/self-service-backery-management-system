<template>
  <div class="login_container">
    <el-row>
      <el-col :span="8" :xs="0"></el-col>
      <el-col :span="12" :xs="24">
        <el-form
          class="login_form"
          :model="loginInfo"
          :rules="rules"
          ref="loginForm"
        >
          <h1>Hello</h1>
          <h2>欢迎来到面包店</h2>
          <el-form-item prop="username">
            <el-input
              :prefix-icon="User"
              v-model="loginInfo.username"
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              :prefix-icon="Lock"
              type="password"
              v-model="loginInfo.password"
              show-password
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="button_l" type="primary" @click="login">
              登录
            </el-button>

            <el-button class="button_r" type="primary" @click="register">
              注册
            </el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import { User, Lock } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
import useUserStore from '@/store/modules/user'

let useStore = useUserStore()
// 获取el-form组件
let loginForm = ref()
// 获取路由器
let $router = useRouter()
// 收集账号与密码
let loginInfo = reactive({
  username: '',
  password: '',
})
// 自定义校验规则函数
const validatorUserName = (_rule: any, value: any, callback: any) => {
  // rule：即为校验规则对象, value: 即为表单元素文本内容, 函数：如果符合条件callback放行通过，不符合则注入错误提示信息
  if (value.length >= 5) {
    callback()
  } else {
    callback(new Error('账号长度至少5位'))
  }
}

// 校验密码
const validatorPwd = (_rule: any, value: any, callback: any) => {
  const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]+$/
  if (value.length >= 6 && passwordRegex.test(value)) {
    callback()
  } else {
    callback(new Error('密码长度至少6位,且只能存在字母数字和部分符号'))
  }
}
// 定义表单校验需要配置对象
const rules = {
  username: [
    // { required: true, message: '账号长度至少为6位', rigger: 'change', min: 6, max: 10,},
    { trigger: 'change', validator: validatorUserName },
  ],
  password: [{ trigger: 'change', validator: validatorPwd }],
}
const login = async () => {
  // 保证全部表单校验通过在发请求
  await loginForm.value.validate()
  try {
    await useStore.userLogin(loginInfo)
    $router.push('/')
    // 登陆成功提示
    ElNotification({
      type: 'success',
      message: '登陆成功',
    })
  } catch (error) {
    // 登陆失败提醒
    ElNotification({
      type: 'error',
      message: (error as Error).message,
    })
  }
}

const register = () => {
  $router.push('/register')
}
</script>

<style scoped>
.login_container {
  width: 100%;
  height: 100vh;
  background: url('@/assets/images/donuts.png') no-repeat;
  background-size: cover;
  padding: none;
}
.login_form {
  width: 70%;
  margin-top: 30vh;
  background: url('@/assets/images/login_form.png');
  padding: 40px;
  h1 {
    color: white;
  }
  h2 {
    color: white;
    margin: 20px 0;
  }
  .button_l {
    width: 45%;
    margin-right: 5%;
  }
  .button_r {
    margin-left: 5%;
    width: 45%;
  }
}
</style>
