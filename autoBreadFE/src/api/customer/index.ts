// 用户管理模块的接口
import request from '@/utils/request'
import type { CustomerResponseData, Customer } from './type'
// 枚举地址
enum API {
  // 获取全部已有顾客账号信息
  ALLCUSTOMER_URL = '/customer/',
  // 添加
  ADDCUSTOMER_URL = '/customer/add/',
  // 修改
  UPDATECUSTOMER_URL = '/customer/update/',
  // 删除
  DELETE_URL = '/customer/remove/',
}
// 获取用户账号信息的接口
export const reqAllCustomer = (
  page: number,
  limit: number,
  customerId: number,
) =>
  request.get<any, CustomerResponseData>(
    API.ALLCUSTOMER_URL + `${page}/${limit}/?customerId=${customerId}`,
  )

// 添加用户接口方法
export const reqAddCustomer = (data: Customer) => {
  return request.post<any, any>(API.ADDCUSTOMER_URL, data)
}

// 修改用户接口方法
export const reqUpdateCustomer = (data: Customer) => {
  return request.put<any, any>(API.UPDATECUSTOMER_URL + `${data.id}/`, data)
}

// 删除顾客接口方法
export const reqDeleteCustomer = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + id)
}
