<template>
  <el-icon style="margin-right: 10px" @click="changeIcon">
    <component :is="LayOutSettingStore.fold ? 'Fold' : 'Expand'"></component>
  </el-icon>
  <el-breadcrumb separator-icon="ArrowRight">
    <el-breadcrumb-item
      v-for="(item, index) in $route.matched"
      :key="index"
      v-show="item.meta.title"
      :to="item.path"
    >
      <el-icon>
        <component :is="item.meta.icon"></component>
      </el-icon>
      <span style="margin: 0px 5px">{{ item.meta.title }}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script lang="ts" setup name="Breadcrumb">
import { useRoute } from 'vue-router'
// 点击图标收缩菜单栏
import useLayOutSettingStore from '@/store/modules/setting'
// 获取layout配置相关的仓库
let LayOutSettingStore = useLayOutSettingStore()
let $route = useRoute()
const changeIcon = () => {
  LayOutSettingStore.fold = !LayOutSettingStore.fold
}
</script>

<style scoped></style>
