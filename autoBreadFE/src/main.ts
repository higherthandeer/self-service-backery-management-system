import { createApp } from 'vue'
import App from '@/App.vue'
// 引入elementUI-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 配置element-plus国际化
//@ts-ignore忽略当前文件ts类型的检测否则有红色提示(打包会失败)
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// svg插件需要
import 'virtual:svg-icons-register'
// 引入自定义插件对象：注册整个项目全局组件
import globalComponent from '@/components'
// 引入路由
import router from './router'
// 引入仓库
import pinia from './store'
// 引入路由鉴权文件
import './permission'
// 引入自定义指令文件
import { isHasButton } from './directive/hasButton'

const app = createApp(App)
app.use(ElementPlus, {
  locale: zhCn,
})

// 安装自定义插件
app.use(globalComponent)
app.use(router)
app.use(pinia)

isHasButton(app)

app.mount('#app')
