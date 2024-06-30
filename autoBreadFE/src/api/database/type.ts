// 账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
// 一个用户账号信息ts类型
export interface Backup {
  [key: string]: any
  id?: number
  backup_name?: string
  backup_date?: string
  backup_description?: string
  backup_file?: string
}
// 全部用户信息
export type Records = Backup[]

export interface BackupResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    size: number
    current: number
    pages: number
  }
}
