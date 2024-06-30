// 销售单管理模块接口
import request from '@/utils/request'
import { ReceiptResponseData } from './type'
// 销售单管理模块接口地址
enum API {
  RECEIPT_URL = '/sell/receipt/info/',
}
// page: 获取第几页 limit: 获取几个已有订单的数据
export const reqAllReceipt = (page: number, limit: number) =>
  request.get<any, ReceiptResponseData>(API.RECEIPT_URL + `${page}/${limit}/`)
