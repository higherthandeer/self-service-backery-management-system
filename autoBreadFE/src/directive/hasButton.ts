import pinia from '@/store'
import useUserStore from '@/store/modules/user'

let userStore = useUserStore(pinia)
export const isHasButton = (app: any) => {
  // 获取对应用户仓库
  // 全局自定义指令
  app.directive('hasButton', {
    mounted(el: any, options: any) {
      if (!userStore.buttons.includes(options.value)) {
        el.parentNode.removeChild(el)
      }
    },
  })
}
