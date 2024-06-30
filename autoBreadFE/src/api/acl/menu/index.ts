// 权限管理模块接口
import request from '@/utils/request'
import type { PermissionResponseData, MenuParams } from './type'

enum API {
  // 获取全部菜单和按钮
  ALLPERMISSION_URL = '/acl/permission/',
  // 新增子菜单
  ADDMENU_URL = '/acl/permission/add/',
  // 更新菜单
  UPDATEMENU_URL = '/acl/permission/update/',
  // 删除菜单
  DELETEMENU_URL = '/acl/permission/remove/',
}
// 获取菜单数据
export const reqAllPermission = () => {
  return request.get<any, PermissionResponseData>(API.ALLPERMISSION_URL)
}
// 添加菜单接口方法
export const reqAddMenu = (data: MenuParams) => {
  return request.post<any, any>(API.ADDMENU_URL, data)
}

// 修改用户接口方法
export const reqUpdateMenu = (data: MenuParams) => {
  return request.put<any, any>(API.UPDATEMENU_URL + `${data.id}/`, data)
}

// 删除用户接口方法
export const reqDeleteMenu = (id: number) => {
  return request.delete<any, any>(API.DELETEMENU_URL + id)
}
