// 商品管理模块接口
import request from '@/utils/request'
import type { GoodsResponseData, Goods } from './type'
// 品牌管理模块接口地址
enum API {
  GOODS_URL = '/goods/info/',
  ADDGOODS_URL = '/goods/add/',
  UPDATEGOODS_URL = '/goods/update/',
  DELETE_URL = '/goods/remove/',
  EXPIRE_URL = '/goods/expire/',
}
// 获取已有品牌的接口方法
// page: 获取第几页 limit: 获取几个已有品牌的数据
export const reqHasGoods = (page: number, limit: number, breadname: string) =>
  request.get<any, GoodsResponseData>(
    API.GOODS_URL + `${page}/${limit}/?breadname=${breadname}`,
  )

// 添加商品接口方法
export const reqAddGoods = (data: Goods) => {
  return request.post<any, any>(API.ADDGOODS_URL, data)
}

// 修改商品接口方法
export const reqUpdateGoods = (data: Goods) => {
  return request.put<any, any>(API.UPDATEGOODS_URL + `${data.id}/`, data)
}

// 删除商品接口方法
export const reqDeleteGoods = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + `${id}/`)
}
export const reqExpireGoods = () => request.get<any, any>(API.EXPIRE_URL)
