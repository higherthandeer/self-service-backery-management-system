// 用户管理模块的接口
import request from '@/utils/request'
import type {
  UserResponseData,
  User,
  AllRoleResponseData,
  SetRoleData,
} from './type'
// 枚举地址
enum API {
  // 获取全部已有用户账号信息
  ALLUSER_URL = '/acl/user/',
  // 添加
  ADDUSER_URL = '/acl/user/add/',
  // 修改
  UPDATEUSER_URL = '/acl/user/update/',
  // 删除
  DELETE_URL = '/acl/user/remove/',
  // 批量删除
  DELETEALL_URL = '/acl/user/batchRemove/',
  // 获取全部角色以及当前角色
  ALLROLE_URL = '/acl/user/get/role/',
  // 设置角色URL
  SETROLE_URL = '/acl/user/set/role/',
  // 重置密码URL
  RESETPWD_URL = '/acl/user/reset/pwd/',
}
// 获取用户账号信息的接口
export const reqAllUser = (page: number, limit: number, username: string) =>
  request.get<any, UserResponseData>(
    API.ALLUSER_URL + `${page}/${limit}/?username=${username}`,
  )

// 添加用户接口方法
export const reqAddUser = (data: User) => {
  return request.post<any, any>(API.ADDUSER_URL, data)
}

// 修改用户接口方法
export const reqUpdateUser = (data: User) => {
  return request.put<any, any>(API.UPDATEUSER_URL + `${data.id}/`, data)
}

// 删除用户接口方法
export const reqDeleteUser = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + id)
}
// 批量删除
export const reqDeleteBatchUser = (idList: number[]) => {
  // return request.delete<any, any>(API.DELETE_URL + `${idList}/`)
  return request.delete<any, any>(API.DELETEALL_URL + idList)
}
// 获取全部角色以及当前角色
export const reqAllRole = (id: number) => {
  return request.get<any, AllRoleResponseData>(API.ALLROLE_URL + `${id}/`)
}
// 分配角色
export const reqSetUserRole = (data: SetRoleData) => {
  return request.post<any, any>(API.SETROLE_URL, data)
}
// 分配角色
export const reqResetPwd = (id: number) => {
  return request.post<any, any>(API.RESETPWD_URL, id)
}
