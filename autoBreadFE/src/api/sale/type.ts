// 后端调用摄像头返回的ts数据类型
export interface DetectResponseData {
  [key: string]: any
  img: string
  txt?: Text[]
}

// 包含全部商品数据的ts类型
export type Text = {
  name: string
  count: number
  price: number
}

export interface ResponseData {
  code: number
  message: string
  data: null
  ok: boolean
}
