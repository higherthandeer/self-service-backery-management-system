// 销售统计
import request from '@/utils/request'
// import { DetailtResponseData } from './type'
// 销售单管理模块接口地址
enum API {
  HEADER_URL = '/sell/detail/header/',
  YEAR_URL = '/sell/per/year/',
  MONTH_URL = '/sell/per/month/',
  DAY_URL = '/sell/per/day/',
  CATAGORY_URL = '/sell/catagory/',
}
// 获取已有品牌的接口方法
// page: 获取第几页 limit: 获取几个已有订单的数据
export const reqHeader = () => request.get<any, any>(API.HEADER_URL)
// 每年
export const reqSellPerYear = () => request.get<any, any>(API.YEAR_URL)
export const reqSellPerMonth = (year: any) =>
  request.get<any, any>(API.MONTH_URL + `${year}`)
export const reqSellPerDay = (year: any, day: any) =>
  request.get<any, any>(API.DAY_URL + `${year}/${day}/`)
export const reqCatagory = () => request.get<any, any>(API.CATAGORY_URL)
