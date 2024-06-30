// 全局守卫

// 对角色路由权限设置
import router from '@/router'
// 加载进度条
import nprogress from 'nprogress'
import 'nprogress/nprogress.css'
nprogress.configure({ showSpinner: false })
// 获取用户相关的小仓库内部token数据，判断用户是否登陆成功
import useUserStore from './store/modules/user'
import pinia from './store'
import setting from './setting'
let userStore = useUserStore(pinia)
// 前置
router.beforeEach(async (to: any, _from: any, next: any) => {
  // 路由的放行函数
  nprogress.start()
  // 获取token判断用户登录还是未登录
  let token = userStore.token
  // 获取用户名字
  let username = userStore.username
  if (token) {
    if (to.path == '/login') {
      // 登录成功，不能访问login，指向首页
      next({ path: '/' })
    } else {
      // 其他的都能访问
      if (username) {
        // 有用户信息放行
        next()
      } else {
        // 没有用户信息则在守卫处发送请求获取用户信息再放行
        try {
          await userStore.userInfo()
          // 若刷新后是异步路由，有可能获取到用户信息但异步路由还未加载完毕
          next({ ...to })
        } catch (error) {
          // token过期
          // 退出登录
          await userStore.userLogout()
          next({ path: '/login' })
        }
      }
    }
  } else {
    if (to.path == '/login' || to.path == '/register') {
      next()
    } else {
      next({ path: '/login' })
    }
  }
})

// 后置
router.afterEach((to: any, _from: any, _next: any) => {
  document.title = `${setting.title} - ${to.meta.title}`
  nprogress.done()
})

// 未登录只能访问登陆页面
// 登录了不能访问登陆页面
