// 商品管理模块接口
import request from '@/utils/request'
import type { InventoryResponseData, Inventory } from './type'
// 品牌管理模块接口地址
enum API {
  INVENTORY_URL = '/inventory/info/',
  ADDINVENTORY_URL = '/inventory/add/',
  UPDATEINVENTORY_URL = '/inventory/update/',
  OUTINV_URL = '/inventory/out/',
  DELETE_URL = '/inventory/remove/',
  EXPIRE_URL = '/inventory/expire/',
  HEADER_URL = '/inventory/statistics/header/',
  VALUECATEGORY_URL = '/inventory/statistics/value/',
  COUNTCATEGORY_URL = '/inventory/statistics/count/',
}
// 获取已有品牌的接口方法
// page: 获取第几页 limit: 获取几个已有品牌的数据
export const reqHasInventory = (
  page: number,
  limit: number,
  breadname: string,
) =>
  request.get<any, InventoryResponseData>(
    API.INVENTORY_URL + `${page}/${limit}/?breadname=${breadname}`,
  )
// 库存统计头部信息
export const reqInventoryHeader = () =>
  request.get<any, InventoryResponseData>(API.HEADER_URL)
// 库存统计各种类价值损失
export const reqInventoryValueCate = () =>
  request.get<any, InventoryResponseData>(API.VALUECATEGORY_URL)
// 库存统计各种类总数
export const reqInventoryCountCate = () =>
  request.get<any, InventoryResponseData>(API.COUNTCATEGORY_URL)

// 添加库存接口方法
export const reqAddInventory = (data: Inventory) => {
  return request.post<any, any>(API.ADDINVENTORY_URL, data)
}

// 修改库存接口方法
export const reqUpdateInventory = (data: Inventory) => {
  return request.put<any, any>(API.UPDATEINVENTORY_URL + `${data.id}/`, data)
}

export const reqOutInventory = (data: Inventory) => {
  return request.post<any, any>(API.OUTINV_URL, data)
}

// 删除库存接口方法
export const reqDeleteInventory = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + `${id}/`)
}
export const reqExpireInv = () => request.get<any, any>(API.EXPIRE_URL)
