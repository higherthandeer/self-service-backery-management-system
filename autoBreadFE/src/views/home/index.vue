<template>
  <div>
    <el-card>
      <div class="box">
        <img :src="userStore.avatar" alt="" class="avatar" />
        <div class="bottom">
          <h1 class="title">你好{{ userStore.username }}</h1>
        </div>
      </div>
    </el-card>
    <div class="backimg">
      <svg-icon name="welcome" width="500px" height="400px"></svg-icon>
    </div>
  </div>
</template>

<script lang="ts" setup name="">
// 引入仓库获取用户头像，昵称
import useUserStore from '@/store/modules/user'
// 存储获取用户信息的仓库对象
let userStore = useUserStore()
</script>

<style scoped>
.box {
  align-items: center;
  display: flex;
  .avatar {
    height: 100px;
    width: 100px;
    border-radius: 50%;
  }
  .bottom {
    margin-left: 20px;
    .title {
      font-size: 30px;
    }
  }
}
.backimg {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
</style>
