// 菜单按钮数据ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
export interface Permission {
  id: number
  pid: number
  name: string
  // code: string
  // tocode: string
  // type: number
  // status: null
  level: number
  children?: PermissionList
  select: boolean
}

export type PermissionList = Permission[]

// 权限数据返回类型
export interface PermissionResponseData extends ResponseData {
  data: PermissionList
}

// 添加与删除彩带携带的参数ts类型
export interface MenuParams {
  id?: number
  pid?: number
  code: string
  level: number
  name: string
}
