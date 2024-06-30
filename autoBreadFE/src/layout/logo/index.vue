<template>
  <div class="logo" v-if="setting.logoShow">
    <img :src="setting.logo" />
    <p v-show="!LayOutSettingStore.fold">{{ setting.title }}</p>
  </div>
</template>

<script lang="ts" setup name="Logo">
import setting from '@/setting'
import useLayOutSettingStore from '@/store/modules/setting'

let LayOutSettingStore = useLayOutSettingStore()
</script>

<style scoped>
.logo {
  width: 100%;
  height: var(--base-menu-logo-heigh);
  color: white;
  display: flex;
  align-items: center;
  padding: 5px;
  img {
    width: 40px;
    height: 40px;
  }
  p {
    font-size: var(--base-logo-title-fontSize);
    margin-left: 5px;
  }
}
</style>
