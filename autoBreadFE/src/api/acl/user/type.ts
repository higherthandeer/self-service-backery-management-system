// 账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// 一个用户账号信息ts类型
export interface User {
  [key: string]: any
  id?: number
  name?: string
  username?: string
  password?: string
  gender?: number
  mobile?: number
  email?: string
  birthday?: string
  avatar?: string
}
// 全部用户信息
export type Records = User[]

export interface UserResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    columns: any
    size: number
    current: number
    pages: number
  }
}

// 一个角色的ts类型
export interface RoleData {
  id?: number
  name: string
}

// 全部职位列表
export type AllRole = RoleData[]

// 获取全部职位的接口返回的数据ts类型
export interface AllRoleResponseData extends ResponseData {
  data: {
    curRoles: AllRole
    allRolesList: AllRole
  }
}

// 给用户分配职位携带参数ts类型
export interface SetRoleData {
  roleIdList: number[]
  userId: number
}
