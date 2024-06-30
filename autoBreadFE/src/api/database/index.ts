// 数据库备份管理模块的接口
import request from '@/utils/request'
import type { BackupResponseData, Backup } from './type'
// 枚举地址
enum API {
  // 获取全部已有数据库备份账号信息
  ALLBACKUP_URL = '/database/',
  // 添加
  ADDBACKUP_URL = '/database/add/',
  // 恢复
  RESTOREBACKUP_URL = '/database/restore/',
  // 删除
  DELETE_URL = '/database/remove/',
  // 批量删除
  DELETEALL_URL = '/database/batchRemove/',
}
// 获取数据库备份账号信息的接口
export const reqAllBackup = (page: number, limit: number, backupName: string) =>
  request.get<any, BackupResponseData>(
    API.ALLBACKUP_URL + `${page}/${limit}/?backupName=${backupName}`,
  )

// 添加数据库备份接口方法
export const reqAddBackup = (data: Backup) => {
  return request.post<any, any>(API.ADDBACKUP_URL, data)
}

// 删除数据库备份接口方法
export const reqRestoreBackup = (id: number) => {
  return request.post<any, any>(API.RESTOREBACKUP_URL, { id: id })
}

// 删除数据库备份接口方法
export const reqDeleteBackup = (id: number) => {
  return request.delete<any, any>(API.DELETE_URL + id)
}
// 批量删除
export const reqDeleteBatchBackup = (idList: number[]) => {
  // return request.delete<any, any>(API.DELETE_URL + `${idList}/`)
  return request.delete<any, any>(API.DELETEALL_URL + idList)
}
