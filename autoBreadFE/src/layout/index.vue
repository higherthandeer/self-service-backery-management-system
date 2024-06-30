<template>
  <div class="layout_container">
    <!-- 左侧菜单 -->
    <div class="layout_slider" :class="{ fold: LayOutSettingStore.fold }">
      <Logo></Logo>
      <el-scrollbar class="scrollbar">
        <!-- 菜单组件 -->
        <el-menu
          :collapse="LayOutSettingStore.fold"
          :default-active="$route.path"
          background-color="#001529"
          text-color="white"
        >
          <!-- 根据路由动态生成菜单 -->
          <Menu :menuList="userStore.menuRoutes"></Menu>
        </el-menu>
      </el-scrollbar>
    </div>
    <!-- 顶部导航 -->
    <div class="layout_tabbar" :class="{ fold: LayOutSettingStore.fold }">
      <Tabbar></Tabbar>
    </div>
    <!-- 内容展示区域 -->
    <div class="layout_main" :class="{ fold: LayOutSettingStore.fold }">
      <Main></Main>
    </div>
  </div>
</template>

<script lang="ts" setup name="Layout">
// 获取路由对象
import { useRoute } from 'vue-router'
// 引入全局样式
import Logo from './logo/index.vue'
// 引入菜单组件
import Menu from './menu/index.vue'
import Tabbar from './tabbar/index.vue'
import Main from './main/index.vue'

// 获取用户相关的小仓库
import useUserStore from '@/store/modules/user'
// 获取折叠菜单栏信息仓库
import useLayOutSettingStore from '@/store/modules/setting'
let userStore = useUserStore()
let LayOutSettingStore = useLayOutSettingStore()

let $route = useRoute()

// console.log($route.path)
</script>

<!-- 安装一下插件使name可只写一个script标签 -->
<!-- npm i vite-plugin-vue-setup-extend -D -->
<!-- <script lang="ts">
export default {
  name: 'Layout',
}
</script> -->

<style scoped>
.layout_container {
  width: 100%;
  height: 100vh;
  .layout_slider {
    color: white;
    width: var(--base-menu-width);
    height: 100vh;
    background-color: var(--base-menu-background);
    transition: all 0.3s;
    .scrollbar {
      width: 100%;
      height: calc(100vh - var(--base-menu-logo-height));
      .el-menu {
        border-right: none;
      }
    }
    &.fold {
      width: var(--base-menu-min-width);
    }
  }
  .layout_tabbar {
    position: fixed;
    top: 0px;
    left: var(--base-menu-width);
    height: var(--base-tabbar-height);
    width: calc(100% - var(--base-menu-width));
    transition: all 0.3s;
    /* background: cyan; */
    &.fold {
      width: calc(100vw - var(--base-menu-min-width));
      left: var(--base-menu-min-width);
    }
  }
  .layout_main {
    position: fixed;
    top: var(--base-tabbar-height);
    left: var(--base-menu-width);
    height: calc(100vh - var(--base-tabbar-height));
    width: calc(100% - var(--base-menu-width));
    padding: 20px;
    overflow: auto;
    transition: all 0.3s;
    &.fold {
      width: calc(100vw - var(--base-menu-min-width));
      left: var(--base-menu-min-width);
    }
  }
}
</style>
