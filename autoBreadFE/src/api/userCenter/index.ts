// 统一管理用户接口
import request from '@/utils/request'

import type { userCenterResponseData, userUpdateResponseData } from './type'

//项目用户相关的请求地址

enum API {
  USERCENTER_URL = '/user/center/',
  AVATAR_URL = '/avatar/',
}

// 获取展示用户中心所需要信息
export const reqUserCenter = () =>
  request.get<any, userCenterResponseData>(API.USERCENTER_URL)

// 发送修改请求
export const reqUpdateUserCenter = (key: string, value: any) =>
  request.post<any, userUpdateResponseData>(API.USERCENTER_URL, {
    key: key,
    value: value,
  })

export const reqUpdateAvatar = (formData: any) =>
  request.post<any, userUpdateResponseData>(API.AVATAR_URL, formData)
