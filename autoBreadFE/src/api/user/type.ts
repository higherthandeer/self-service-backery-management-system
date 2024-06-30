// 登录接口需要携带的参数ts类型

// 看后端传入的数据类型
export interface loginInfo {
  username: string
  password: string
}

export interface registerInfo {
  username: string
  password: string
}

// 全部接口返回数据都拥有的ts类型
export default interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// tokentype
// 登录接口返回数据类型
export interface loginResponseData extends ResponseData {
  // 成功
  data: string
}

export interface registerResponseData extends ResponseData {
  // 成功
  data: string
}

// 服务器返回用户信息相关的数据类型

export interface userInfoReponseData extends ResponseData {
  code: number
  data: {
    username: string
    avatar: string
    routes: string
    buttons: string[]
  }
}
// 登陆接口返回的数据类型
