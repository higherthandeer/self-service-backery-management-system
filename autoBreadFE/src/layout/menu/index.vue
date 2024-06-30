<template>
  <template v-for="(item, _index) in menuList" :key="item.path">
    <!-- 没有子路由 -->
    <el-menu-item
      v-show="!item.meta.hidden"
      v-if="!item.children"
      :index="item.path"
      @click="goRoute"
    >
      <el-icon>
        <component :is="item.meta.icon"></component>
      </el-icon>
      <template #title>
        <span>{{ item.meta.title }}</span>
      </template>
    </el-menu-item>
    <!-- 有子路由但只有一个 -->
    <el-menu-item
      v-show="!item.meta.hidden"
      v-if="item.children && item.children.length == 1"
      :index="item.children[0].path"
      @click="goRoute"
    >
      <el-icon>
        <component :is="item.children[0].meta.icon"></component>
      </el-icon>
      <template #title>
        <span>{{ item.children[0].meta.title }}</span>
      </template>
    </el-menu-item>
    <!-- 有子路由且个数大于一个 -->
    <el-sub-menu
      v-show="!item.meta.hidden"
      :index="item.path"
      v-if="item.children && item.children.length > 1"
    >
      <template #title>
        <el-icon>
          <component :is="item.meta.icon"></component>
        </el-icon>
        <span>{{ item.meta.title }}</span>
      </template>
      <Menu :menuList="item.children"></Menu>
    </el-sub-menu>
  </template>
</template>

<script lang="ts" setup name="Menu">
import { useRouter } from 'vue-router'
// 获取父组件传递过来的全部路由数组
defineProps(['menuList'])

// 获取路由器对象
let $router = useRouter()
const goRoute = (vc: any) => {
  // console.log(vc)
  // console.log(vc.index)
  $router.push(vc.index)
}
</script>

<!-- <script lang="ts">
export default {
  name: 'Menu',
}
</script> -->

<style scoped></style>
