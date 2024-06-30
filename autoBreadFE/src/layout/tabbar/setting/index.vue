<template>
  <el-button
    size="small"
    icon="Refresh"
    circle
    @click="updateRefresh"
  ></el-button>
  <el-button
    size="small"
    icon="FullScreen"
    circle
    @click="changeFullScreen"
  ></el-button>
  <el-button size="small" icon="Setting" circle></el-button>
  <img
    :src="UserStore.avatar"
    style="width: 24px; height: 24px; margin: 0px 10px; border-radius: 50%"
  />
  <!-- 下拉菜单 -->
  <el-dropdown>
    <span class="el-dropdown-link">
      {{ UserStore.username }}
      <el-icon class="el-icon--right">
        <arrow-down />
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="userCenter">个人中心</el-dropdown-item>
        <el-dropdown-item @click="updatePassword">修改密码</el-dropdown-item>
        <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup name="Setting">
import { useRouter } from 'vue-router'
import useLayOutSettingStore from '@/store/modules/setting'
// 获取用户相关信息库
import useUserStore from '@/store/modules/user'
// 获取layout配置相关的仓库
let LayOutSettingStore = useLayOutSettingStore()
let UserStore = useUserStore()
// 获取路由对象
let $router = useRouter()
// 刷新按钮
const updateRefresh = () => {
  LayOutSettingStore.refresh = !LayOutSettingStore.refresh
}
// 全屏
const changeFullScreen = () => {
  let full = document.fullscreenElement
  // 切换全局模式
  if (!full) {
    document.documentElement.requestFullscreen()
  } else {
    // 退出全屏
    document.exitFullscreen()
  }
}
// 退出登录
const logout = async () => {
  // 1.向服务器发送请求，退出登录接口告诉其token无效
  // 2.仓库中关于用户相关的数据清空
  // 3.跳转到登陆页面
  await UserStore.userLogout()
  // 跳转登陆页面
  $router.replace({ path: '/login' })
}
// 个人中心
const userCenter = async () => {
  // 1.向服务器发送请求，退出登录接口告诉其token无效
  // 2.仓库中关于用户相关的数据清空
  // 3.跳转到登陆页面
  // await UserStore.userLogout()

  console.log('用户中心')
  // 跳转用户中心页面
  $router.push({ path: '/user/center' })
}
// 修改面膜
const updatePassword = async () => {
  $router.push({ path: '/update/pwd' })
}
</script>
<style scoped></style>
