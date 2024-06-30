// 关于layout组件相关配置仓库
import { defineStore } from 'pinia'

let useLayOutSettingStore = defineStore('SettingStore', {
  state: () => {
    return {
      fold: false,
      refresh: false, //控制刷新
    }
  },
})

export default useLayOutSettingStore
