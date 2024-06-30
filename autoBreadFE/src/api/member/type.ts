export interface ResponseData {
  code: number
  message: string
  ok: boolean
}

export interface Item {
  breadname: string
  price: number
  quantity: number
  sub_total: string
}

// 已有商品的ts数据类型
export interface Receipt {
  [key: string]: any
  id: number
  date: string
  total: number
  detail: Item[]
}

// 包含全部商品数据的ts类型
export type Records = Receipt[]

// 获取已有全部商品的数据ts类型
export interface ReceiptResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    columns: any
    size: number
    current: number
    pages: number
  }
}

// 一个会员账号信息ts类型
export interface Member {
  [key: string]: any
  id?: number
  name?: string
  username?: string
  level: number
  discount?: string
}
