// 统一管理用户接口
import request from '@/utils/request'

import type {
  loginInfo,
  loginResponseData,
  userInfoReponseData,
  registerInfo,
  registerResponseData,
} from './type'

//项目用户相关的请求地址

enum API {
  LOGIN_URL = '/login/',

  REGISTER_URL = '/register/',

  USERINFO_URL = '/user/info/',

  LOGOUT_URL = '/logout/',
}
// 登录接口
export const reqLogin = (data: loginInfo) =>
  request.post<any, loginResponseData>(API.LOGIN_URL, data) // ??any??

// 注册接口
export const reqRegister = (data: registerInfo) =>
  request.post<any, registerResponseData>(API.REGISTER_URL, data)
// 获取用户信息

export const reqUserInfo = () =>
  request.get<any, userInfoReponseData>(API.USERINFO_URL)

// 退出登录

export const reqLogout = () => request.post<any, any>(API.LOGOUT_URL)
