export interface ResponseData {
  code: number
  message: string
  ok: boolean
}

// 已有商品的ts数据类型
export interface userCenterInfo {
  [key: string]: any
  username: string
  name: string
  gender: number
  mobile: number
  email: string
  birthday: string
}

// 获取用户中心的数据ts类型
export interface userCenterResponseData extends ResponseData {
  data: userCenterInfo
}

// 修改完成返回信息
export interface userUpdateResponseData extends ResponseData {
  data: null
}

export interface userAvatarResponseData extends ResponseData {
  data: { avatar: string }
}
