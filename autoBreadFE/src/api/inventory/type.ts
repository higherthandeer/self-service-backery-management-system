export interface ResponseData {
  code: number
  message: string
  ok: boolean
}

// 已有商品的ts数据类型
export interface Inventory {
  [key: string]: any
  id?: number
  breadname: string
  price: number
  MFG_date: string
  shield_life: number
  count: number
  out_count: number
  is_expired: boolean
}

// 包含全部商品数据的ts类型
export type Records = Inventory[]

// 获取已有全部商品的数据ts类型
export interface InventoryResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    columns: any
    size: number
    current: number
    pages: number
  }
}
