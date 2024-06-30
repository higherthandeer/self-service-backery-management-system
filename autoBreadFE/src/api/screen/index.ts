// 统一管理用户接口
import request from '@/utils/request'

//项目用户相关的请求地址

enum API {
  ADD_INVURL = '/inventory/add/',
}
//登录接口
export const reqAddInv = (data: any) => {
  return request.post<any, any>(API.ADD_INVURL, data) // ??any??
}
