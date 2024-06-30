<template>
  <svg :style="{ width, height }">
    <use :xlink:href="prefix + name" :fill="color"></use>
  </svg>
</template>

<script lang="ts" setup name="">
// 接收父组件传递过来的参数
defineProps({
  // xlink:href属性前缀
  prefix: {
    type: String,
    default: '#icon-',
  },
  // 提供使用的图标名字
  name: String,
  // 颜色
  color: {
    type: String,
    default: '',
  },
  // 大小

  width: {
    type: String,
    default: '16px',
  },
  height: {
    type: String,
    default: '16px',
  },
})
</script>

<style scoped></style>
