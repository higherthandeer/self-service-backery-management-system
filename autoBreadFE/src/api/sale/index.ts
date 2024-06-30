// 统一管理销售接口
import request from '@/utils/request'
import { ResponseData } from '@/api/sale/type.ts'

//项目用户相关的请求地址

enum API {
  SALE_URL = '/goods/sale/',
}
//登录接口
export const reqSale = (data: any) => {
  return request.post<any, ResponseData>(API.SALE_URL, data)
}
