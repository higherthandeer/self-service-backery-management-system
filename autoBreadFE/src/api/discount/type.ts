// 账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// 一个用户账号信息ts类型
export interface Discount {
  [key: string]: any
  id?: number
  level?: number
  discount: string
}
// 全部用户信息
export type Records = Discount[]

export interface DiscountResponseData extends ResponseData {
  data: {
    records: Records
    columns: any
  }
}
