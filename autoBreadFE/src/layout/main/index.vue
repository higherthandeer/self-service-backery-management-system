<template>
  <!-- 路由组件出口的位置 -->
  <router-view v-slot="{ Component }">
    <transition name="fade">
      <component :is="Component" v-if="flag"></component>
    </transition>
  </router-view>
</template>

<script lang="ts" setup name="Main">
import { watch, ref, nextTick } from 'vue'
import useLayOutSettingStore from '@/store/modules/setting'

let LayOutSettingStore = useLayOutSettingStore()

// 控制当前组件是否销毁重建
let flag = ref(true)
// 监听仓库内部数据refresh是否变化若变化说明点击刷新按钮
watch(
  () => LayOutSettingStore.refresh,
  () => {
    // 点击刷新按钮：路由组件销毁
    flag.value = false
    nextTick(() => {
      flag.value = true
    })
  },
)
</script>

<style scoped>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-active {
  transition: all 1s;
}
.fade-enter-to {
  opacity: 1;
}
</style>
