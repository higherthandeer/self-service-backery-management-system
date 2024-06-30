<template>
  <div>
    <el-card>
      <div class="userHeader">
        <img :src="userStore.avatar" alt="" class="avatar" />
        <div class="username">{{ userStore.username }}</div>
        <div class="btn">
          <div class="upload">
            <el-upload
              accept=".jpg,.png"
              :data="uploadParam"
              :on-success="handleAvatarSucces"
              :action="uploadURL"
              :before-upload="beforeAvatarUpload"
              :show-file-list="false"
            >
              <template #trigger>
                <el-button type="primary">修改头像</el-button>
              </template>
            </el-upload>
          </div>
          <!-- <el-button type="primary">修改头像</el-button> -->
          <router-link to="/update/pwd/">
            <el-button type="primary">修改密码</el-button>
          </router-link>
        </div>
      </div>
    </el-card>
    <el-card class="information">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <el-form ref="formRef" :model="userParams" :rules="rules">
        <ul>
          <li
            class="item"
            @mouseover="handleMouseOver('Uname')"
            @mouseleave="handleMouseLeave('Uname')"
          >
            <div class="title">用户名</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isUnameEdit">
                {{ userInfo.username }}
              </div>
              <el-form-item v-show="isUnameEdit" prop="username">
                <el-input
                  v-model="userParams.username"
                  placeholder="请输入用户名"
                ></el-input>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showUnameBtn && !isUnameEdit"
                size="small"
                @click="handleEdit('Uname')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isUnameEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Uname', userParams.username)"
              >
                确认
              </el-button>
              <el-button
                v-show="isUnameEdit"
                size="small"
                @click="isUnameEdit = !isUnameEdit"
              >
                取消
              </el-button>
            </div>
          </li>
          <li
            class="item"
            @mouseover="handleMouseOver('Name')"
            @mouseleave="handleMouseLeave('Name')"
          >
            <div class="title">真实姓名</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isNameEdit">
                {{ userInfo.name }}
              </div>
              <el-form-item v-show="isNameEdit" prop="name">
                <el-input
                  v-model="userParams.name"
                  placeholder="请输入真实姓名"
                ></el-input>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showNameBtn && !isNameEdit"
                size="small"
                @click="handleEdit('Name')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isNameEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Name', userParams.name)"
              >
                确认
              </el-button>
              <el-button
                v-show="isNameEdit"
                size="small"
                @click="isNameEdit = !isNameEdit"
              >
                取消
              </el-button>
            </div>
          </li>
          <li
            class="item"
            @mouseover="handleMouseOver('Gender')"
            @mouseleave="handleMouseLeave('Gender')"
          >
            <div class="title">性别</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isGenderEdit">
                {{ userInfo.gender == 1 ? '男' : '女' }}
              </div>
              <el-form-item v-show="isGenderEdit">
                <el-radio-group v-model="userParams.gender" class="ml-4">
                  <el-radio :label="1">男</el-radio>
                  <el-radio :label="2">女</el-radio>
                </el-radio-group>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showGenderBtn && !isGenderEdit"
                size="small"
                @click="handleEdit('Gender')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isGenderEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Gender', userParams.gender)"
              >
                确认
              </el-button>
              <el-button
                v-show="isGenderEdit"
                size="small"
                @click="isGenderEdit = !isGenderEdit"
              >
                取消
              </el-button>
            </div>
          </li>

          <li
            class="item"
            @mouseover="handleMouseOver('Mobile')"
            @mouseleave="handleMouseLeave('Mobile')"
          >
            <div class="title">手机号码</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isMobileEdit">
                {{ userInfo.mobile }}
              </div>
              <el-form-item v-show="isMobileEdit" prop="mobile">
                <el-input
                  v-model="userParams.mobile"
                  placeholder="请输入手机号码"
                ></el-input>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showMobileBtn && !isMobileEdit"
                size="small"
                @click="handleEdit('Mobile')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isMobileEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Mobile', userParams.mobile)"
              >
                确认
              </el-button>
              <el-button
                v-show="isMobileEdit"
                size="small"
                @click="isMobileEdit = !isMobileEdit"
              >
                取消
              </el-button>
            </div>
          </li>
          <li
            class="item"
            @mouseover="handleMouseOver('Email')"
            @mouseleave="handleMouseLeave('Email')"
          >
            <div class="title">邮件地址</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isEmailEdit">
                {{ userInfo.email }}
              </div>
              <el-form-item v-show="isEmailEdit" prop="email">
                <el-input v-model="userParams.email"></el-input>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showEmailBtn && !isEmailEdit"
                size="small"
                @click="handleEdit('Email')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isEmailEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Email', userParams.email)"
              >
                确认
              </el-button>
              <el-button
                v-show="isEmailEdit"
                size="small"
                @click="isEmailEdit = !isEmailEdit"
              >
                取消
              </el-button>
            </div>
          </li>
          <li
            class="item"
            @mouseover="handleMouseOver('Birthday')"
            @mouseleave="handleMouseLeave('Birthday')"
          >
            <div class="title">生日</div>
            <div class="content">
              <div style="font-size: 17px" v-show="!isBirthdayEdit">
                {{ userInfo.birthday }}
              </div>
              <el-form-item v-show="isBirthdayEdit" prop="birthday">
                <el-date-picker
                  v-model="userParams.birthday"
                  type="date"
                  placeholder="选择日期时间"
                  value-format="YYYY-MM-DD"
                ></el-date-picker>
              </el-form-item>
            </div>
            <div class="edit">
              <el-button
                v-show="showBirthdayBtn && !isBirthdayEdit"
                size="small"
                @click="handleEdit('Birthday')"
              >
                编辑
              </el-button>
              <el-button
                v-show="isBirthdayEdit"
                size="small"
                type="primary"
                @click="updateUserCenter('Birthday', userParams.birthday)"
              >
                确认
              </el-button>
              <el-button
                v-show="isBirthdayEdit"
                size="small"
                @click="isBirthdayEdit = !isBirthdayEdit"
              >
                取消
              </el-button>
            </div>
          </li>
        </ul>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup name="">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, UploadProps } from 'element-plus'
import { reqUserCenter, reqUpdateUserCenter } from '@/api/userCenter'
import {
  userCenterResponseData,
  userCenterInfo,
  userAvatarResponseData,
} from '@/api/userCenter/type'

// 引入仓库获取用户头像，昵称
import useUserStore from '@/store/modules/user'
// 存储获取用户信息的仓库对象
let userStore = useUserStore()
const username: string = userStore.username

// import { ElMessage } from 'element-plus'

// 是否处于编辑状态
let isUnameEdit = ref(false)
let isNameEdit = ref(false)
// let changePWD= ref(false)
let isGenderEdit = ref(false)
let isMobileEdit = ref(false)
let isEmailEdit = ref(false)
let isBirthdayEdit = ref(false)
// 是否处于悬浮状态
let showUnameBtn = ref(false)
let showNameBtn = ref(false)
// let showPWD= ref(false)
let showGenderBtn = ref(false)
let showMobileBtn = ref(false)
let showEmailBtn = ref(false)
let showBirthdayBtn = ref(false)

let userInfo: any = ref({})
// let isShowAvatar = ref(0)

let userParams: userCenterInfo = reactive({
  username: '',
  name: '',
  gender: 1,
  mobile: 1,
  email: '',
  birthday: '',
})

const getUserCenter = async () => {
  let result: userCenterResponseData = await reqUserCenter()
  // console.log(result) // 调试用可注释
  console.log(result)
  if (result.code == 200) {
    // 存储用户信息总数
    userInfo.value = result.data

    // console.log(userParams)
  }
}
// 组件挂载完毕则发请求
onMounted(() => {
  getUserCenter()
})

// 点击编辑
const handleEdit = (value: string) => {
  Object.assign(userParams, userInfo.value)
  clearVali()

  if (value == 'Uname') {
    isUnameEdit.value = !isUnameEdit.value
  }
  if (value == 'Name') {
    isNameEdit.value = !isNameEdit.value
  }
  if (value == 'Mobile') {
    isMobileEdit.value = !isMobileEdit.value
  }
  if (value == 'Email') {
    isEmailEdit.value = !isEmailEdit.value
  }
  if (value == 'Gender') {
    isGenderEdit.value = !isGenderEdit.value
  }
  if (value == 'Birthday') {
    isBirthdayEdit.value = !isBirthdayEdit.value
  }
}
// 处理悬浮
const handleMouseOver = (value: string) => {
  if (value == 'Uname') {
    showUnameBtn.value = true
  }
  if (value == 'Name') {
    showNameBtn.value = true
  }
  if (value == 'Mobile') {
    showMobileBtn.value = true
  }
  if (value == 'Gender') {
    showGenderBtn.value = true
  }
  if (value == 'Email') {
    showEmailBtn.value = true
  }
  if (value == 'Birthday') {
    showBirthdayBtn.value = true
  }
}
const handleMouseLeave = (value: string) => {
  if (value == 'Uname') {
    showUnameBtn.value = false
  }
  if (value == 'Name') {
    showNameBtn.value = false
  }
  if (value == 'Mobile') {
    showMobileBtn.value = false
  }
  if (value == 'Gender') {
    showGenderBtn.value = false
  }
  if (value == 'Email') {
    showEmailBtn.value = false
  }
  if (value == 'Birthday') {
    showBirthdayBtn.value = false
  }
}
// 确认修改
const updateUserCenter = async (key: string, value: any) => {
  if (key == 'Uname') {
    isUnameEdit.value = !isUnameEdit.value
  }
  if (key == 'Name') {
    isNameEdit.value = !isNameEdit.value
  }
  if (key == 'Mobile') {
    isMobileEdit.value = !isMobileEdit.value
  }
  if (key == 'Email') {
    isEmailEdit.value = !isEmailEdit.value
  }
  if (key == 'Gender') {
    isGenderEdit.value = !isGenderEdit.value
  }
  if (key == 'Birthday') {
    isBirthdayEdit.value = !isBirthdayEdit.value
  }
  let result = await reqUpdateUserCenter(key, value)
  console.log(result)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: result.message,
    })
    // 再次发请求获取全部数据
    getUserCenter()
  } else {
    console.log(result)
    ElMessage({
      type: 'error',
      message: result.message,
    })
  }
}

const validatorUserName = (_rule: any, value: any, callback: any) => {
  // rule：即为校验规则对象, value: 即为表单元素文本内容, 函数：如果符合条件callback放行通过，不符合则注入错误提示信息
  const usernameRegex = /^[A-Za-z0-9]{5,}$/
  if (usernameRegex.test(value)) {
    callback()
  } else {
    callback(new Error('用户名只能由字母和数字组成且不能少于5位！'))
  }
}
const validatorName = (_rule: any, value: any, callback: any) => {
  // rule：即为校验规则对象, value: 即为表单元素文本内容, 函数：如果符合条件callback放行通过，不符合则注入错误提示信息
  if (value.length >= 2) {
    callback()
  } else {
    callback(new Error('真实姓名至少2位'))
  }
}
// 电话号码11位且是数字
const validatorMobile = (_rule: any, value: any, callback: any) => {
  // rule：即为校验规则对象, value: 即为表单元素文本内容, 函数：如果符合条件callback放行通过，不符合则注入错误提示信息
  const numberRegex = /^[0-9]+$/
  if (value.length == 11 && numberRegex.test(value)) {
    callback()
  } else {
    callback(new Error('请输入格式正确的手机号码'))
  }
}
// 检查email
const validatorEmail = (_rule: any, value: any, callback: any) => {
  let reg = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/
  if (!reg.test(value)) {
    callback(new Error('请输入正确的邮箱地址'))
  } else {
    callback()
  }
}

// 定义表单校验需要配置对象
const rules = {
  username: [
    // { required: true, message: '账号长度至少为6位', rigger: 'change', min: 6, max: 10,},
    { trigger: 'change', validator: validatorUserName },
  ],
  name: [
    // { required: true, message: '账号长度至少为6位', rigger: 'change', min: 6, max: 10,},
    { trigger: 'change', validator: validatorName },
  ],
  mobile: [{ trigger: 'change', validator: validatorMobile }],
  email: [{ trigger: 'change', validator: validatorEmail }],
  birthday: [{ trigger: 'change', required: true, message: '请输入生产日期' }],
}
// form表单ref，用于清除校验
let formRef = ref()
// 清空校验信息
const clearVali = () => {
  nextTick(() => {
    formRef.value.clearValidate([
      'username',
      'price',
      'MFG_date',
      'sheld_life',
      'count',
      'sale_count',
      'is_expired',
    ])
  })
}
// 头像上传
const uploadURL = 'http://127.0.0.1:8000/api/avatar/'
const uploadParam: object = {
  username: username,
}
const handleAvatarSucces = (response: userAvatarResponseData) => {
  console.log(response)
  if (response.code == 200) {
    userStore.avatar = response.data.avatar
    getUserCenter()
    ElMessage({
      type: 'success',
      message: '修改头像成功',
    })
  } else {
    ElMessage({
      type: 'error',
      message: '修改头像失败',
    })
  }
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  console.log(rawFile)
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('头像必须为jpg或者png！')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('头像大小不能超过2MB！')
    return false
  }
  return true
}
</script>

<style scoped>
ul,
li {
  list-style: none;
}
.information {
  margin-top: 5px;
  .card-header {
    font-weight: bold;
  }
}

.item {
  display: flex;
  align-items: baseline;
  .title {
    font-size: 15px;
    width: 100px;
    height: 50px;
  }
  .content {
    margin-left: 60px;
  }
  .edit {
    margin-left: 60px;
  }
}
.userHeader {
  padding: 10px;
  align-items: center;
  display: flex;
  text-align: center;
  .avatar {
    height: 90px;
    width: 100px;
    border-radius: 50%;
  }
  .username {
    font-size: 30px;
    margin-left: 10px;
  }
  .btn {
    margin-left: 10px;
  }
  .upload {
    display: inline-block;
    margin-right: 10px;
  }
}
.cropper-content {
  .cropper {
    width: auto;
    height: 350px;
    .handle_btn {
      display: flex;
      display: -webkit-flex;
      justify-content: space-between;
      padding: 10px 300px;
      box-sizing: border-box;
    }
  }
}
</style>
