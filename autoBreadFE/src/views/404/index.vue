<template>
  <div class="box">
    <img src="../../assets/images/error_images/404.png" alt="" />
    <el-button type="primary" @click="goHome">首页</el-button>
  </div>
</template>

<script lang="ts" setup name="">
import { useRouter } from 'vue-router'
let $router = useRouter()
const goHome = () => {
  $router.push('/home')
}
</script>

<style scoped>
.box {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  img {
    width: 800px;
    height: 400px;
  }
}
</style>
