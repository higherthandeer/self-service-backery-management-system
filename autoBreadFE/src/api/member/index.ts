// 销售单管理模块接口
import request from '@/utils/request'
// import { ReceiptResponseData } from './type'
// 销售单管理模块接口地址
enum API {
  SHOPPING_URL = '/member/receipt/',
  INFO_URL = '/member/info/',
}
// page: 获取第几页 limit: 获取几个已有订单的数据
export const reqMemberReceipt = (page: number, limit: number) =>
  request.get<any, any>(API.SHOPPING_URL + `${page}/${limit}/`)
// 获取会员信息
export const reqMemberInfo = () => request.get<any, any>(API.INFO_URL)
