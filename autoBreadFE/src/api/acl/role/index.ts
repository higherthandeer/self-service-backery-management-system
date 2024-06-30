// 角色管理模块的接口
import request from '@/utils/request'
import type { RoleResponseData, Role, MenuResponseData } from './type'
// 枚举地址
enum API {
  // 获取全部已有用户账号信息
  ALLROLE_URL = '/acl/role/',
  // 添加
  ADDROLE_URL = '/acl/role/add/',
  // 修改
  UPDATEROLE_URL = '/acl/role/update/',
  // 删除
  DELETE_URL = '/acl/role/remove/',
  // 权限数据
  ALLPERMISSION_URL = '/acl/role/get/permission/',
  // 分配权限
  SETPERMISSION_URL = '/acl/role/set/permission/',
}
// 获取用户账号信息的接口
export const reqAllRole = (page: number, limit: number, name: string) =>
  request.get<any, RoleResponseData>(
    API.ALLROLE_URL + `${page}/${limit}/?rolename=${name}`,
  )

// 添加用户接口方法
export const reqAddRole = (data: Role) => {
  return request.post<any, any>(API.ADDROLE_URL, data)
}

// 修改用户接口方法
export const reqUpdateRole = (data: Role) => {
  return request.put<any, any>(API.UPDATEROLE_URL + `${data.id}/`, data)
}

// 删除用户接口方法
export const reqDeleteRole = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + id)
}
// 获取当前角色的权限
export const reqAllMenuList = (roleId: number) => {
  return request.get<any, MenuResponseData>(API.ALLPERMISSION_URL + roleId)
}

// 给角色设置权限
export const reqSetPermission = (roleId: number, permissionId: number[]) => {
  return request.post<any, any>(API.SETPERMISSION_URL, { roleId, permissionId })
}
