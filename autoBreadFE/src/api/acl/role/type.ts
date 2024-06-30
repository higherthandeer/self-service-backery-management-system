// 账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// 一个职位类型
export interface Role {
  [key: string]: any
  id?: number
  name?: string
}
// 全部职位信息
export type Records = Role[]

export interface RoleResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    columns: any
    size: number
    current: number
    pages: number
  }
}

// 菜单按钮数据ts类型
export interface Menu {
  id: number
  pid: number
  name: string
  // code: string
  // tocode: string
  // type: number
  // status: null
  level: number
  children?: MenuList
  select: boolean
}

export type MenuList = Menu[]

// 菜单权限和按钮权限数据类型
export interface MenuResponseData extends ResponseData {
  data: MenuList
}
