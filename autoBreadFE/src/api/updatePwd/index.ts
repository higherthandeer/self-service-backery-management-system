// 统一管理用户接口
import request from '@/utils/request'

// import type { userCenterResponseData, userUpdateResponseData } from './type'

//项目用户相关的请求地址

enum API {
  UPDATEPWD_URL = '/update/pwd/',
}
// 确认密码

// 修改密码

export const reqUpdatePwd = (value: any) =>
  request.post<any, any>(API.UPDATEPWD_URL, value)
