// 用户管理模块的接口
import request from '@/utils/request'
import type { DiscountResponseData, Discount } from './type'
// 枚举地址
enum API {
  // 获取全部已有折扣账号信息
  ALLDISCOUNT_URL = '/discount/',
  // 添加
  ADDDISCOUNT_URL = '/discount/add/',
  // 修改
  UPDATEDISCOUNT_URL = '/discount/update/',
  // 删除
  DELETE_URL = '/discount/remove/',
}
// 获取用户账号信息的接口
export const reqAllDiscount = () =>
  request.get<any, DiscountResponseData>(API.ALLDISCOUNT_URL)

// 添加用户接口方法
export const reqAddDiscount = (data: Discount) => {
  return request.post<any, any>(API.ADDDISCOUNT_URL, data)
}

// 修改用户接口方法
export const reqUpdateDiscount = (data: Discount) => {
  return request.put<any, any>(API.UPDATEDISCOUNT_URL + `${data.id}/`, data)
}

// 删除顾客接口方法
export const reqDeleteDiscount = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + id)
}
