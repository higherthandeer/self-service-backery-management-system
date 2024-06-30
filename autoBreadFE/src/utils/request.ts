// 进行axios的二次封装
import axios from 'axios'
import { ElMessage } from 'element-plus'
// 引入用户相关的仓库
import useUserStore from '@/store/modules/user'
let request = axios.create({
  // baseURL: 'http://192.168.0.105:8000/api',
  baseURL: 'http://127.0.0.1:8000/api',
  // baseURL: 'http://192.168.157.195:8000/api',
  timeout: 5000, // 设置超时时间
})
// request实例添加请求与响应拦截器
request.interceptors.request.use((config) => {
  // 获取仓库内部的token，登陆成功后携带给服务器
  let userStore = useUserStore()
  // console.log(userStore.token)
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})
//响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    //处理网络错误
    let msg = ''
    let status = error.response.status
    switch (status) {
      case 401:
        msg = 'token过期'
        break
      case 403:
        msg = '无权访问'
        break
      case 404:
        msg = '请求地址错误'
        break
      case 500:
        msg = '服务器出现问题'
        break
      default:
        msg = '无网络'
    }
    ElMessage({
      type: 'error',
      message: msg,
    })
    return Promise.reject(error)
  },
)
export default request
