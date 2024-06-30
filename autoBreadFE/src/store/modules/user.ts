// 创建用户相关仓库
import { defineStore } from 'pinia'
// 引入接口
import { reqLogin, reqUserInfo, reqLogout } from '@/api/user'
// 引入数据类型
import type {
  loginInfo,
  loginResponseData,
  userInfoReponseData,
} from '@/api/user/type'
import type { UserState } from './types/type'
// 引入操作本地存储的工具方法
import { SET_TOKEN, GET_TOKEN, REMOVE_TOKEN } from '@/utils/token'
// 引入路由
import { constantRoute, asyncRoute, anyRoute } from '@/router/routes'
// 引入深拷贝方法
import cloneDeep from 'lodash/cloneDeep'
import router from '@/router'

//用于过滤当前用户需要展示的异步路由
function filterAsyncRoute(asnycRoute: any, routes: any) {
  return asnycRoute.filter((item: any) => {
    if (routes.includes(item.name)) {
      if (item.children && item.children.length > 0) {
        item.children = filterAsyncRoute(item.children, routes)
      }
      return true
    }
  })
}

// 创建用户小仓库
let useUserStore = defineStore('User', {
  // 小仓库存储数据的地方

  state: (): UserState => {
    return {
      token: GET_TOKEN(), // 用户的唯一标识
      menuRoutes: constantRoute, // 仓库存储生成菜单需要的数组(路由)
      username: '',
      avatar: '',
      buttons: [], //存储当前用户按钮表示
    }
  },
  // 异步|逻辑的地方
  actions: {
    // 用户的登录
    async userLogin(data: loginInfo) {
      let result: loginResponseData = await reqLogin(data)
      console.log(result)
      if (result.code == 200) {
        // 登陆成功pinia仓库存储token
        this.token = result.data
        // 本地存储持久化
        // localStorage.setItem('TOKEN', (result.data.token as string))
        SET_TOKEN(result.data)
        return 'ok'
      } else {
        return Promise.reject(new Error(result.data))
      }
    },
    // 获取用户信息
    async userInfo() {
      // 获取用户信息并存储到仓库中
      let result: userInfoReponseData = await reqUserInfo()
      // console.log(result.data)
      if (result.code == 200) {
        this.username = result.data.username
        this.avatar = result.data.avatar
        this.buttons = result.data.buttons
        // 计算当前用户需要展示的异步路由

        let userAsyncRoute = filterAsyncRoute(
          cloneDeep(asyncRoute),
          result.data.routes,
        )
        // console.log(userAsyncRoute)
        // 菜单的数据
        this.menuRoutes = [...constantRoute, ...userAsyncRoute, anyRoute]
        let needRoutes = [...userAsyncRoute, anyRoute]
        needRoutes.forEach((route: any) => {
          router.addRoute(route)
        })
        // console.log(router.getRoutes())
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
    // 退出登录
    async userLogout() {
      // 向后端发送退出登录请求
      let result: any = await reqLogout()
      console.log(result)
      if (result.code == 200) {
        this.token = ''
        this.username = ''
        this.avatar = ''
        REMOVE_TOKEN()
        return 'ok'
      } else {
        return Promise.reject('退出登录失败')
      }
    },
  },
  getters: {},
})

export default useUserStore
