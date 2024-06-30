// 账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// 一个用户账号信息ts类型
export interface Customer {
  [key: string]: any
  id?: number
  name?: string
  username?: string
  level: number
  discount?: string
}
// 全部用户信息
export type Records = Customer[]

export interface CustomerResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    columns: any
    size: number
    current: number
    pages: number
  }
}
