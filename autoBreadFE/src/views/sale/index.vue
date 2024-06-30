<template>
  <div class="box">
    <div class="card">
      <el-card>
        <template #header>
          欢迎来到面包店， 请将商品放置在正确位置
          <div style="max-width: 80%; height: auto; margin-top: 8px">
            <el-button type="primary" @click="initWebSocket">
              打开摄像头
            </el-button>
            <el-button type="primary" @click="closeCamera">
              关闭摄像头
            </el-button>
          </div>
        </template>
        <div class="video-container">
          <div class="box-img" v-show="isCameraOpen">
            <img :src="imageSrc" alt="Camera Stream" />
          </div>
          <!-- 检测目的 -->
          <div>
            <el-card class="box-card">
              <template #header>
                <div class="card-header">
                  <span>商品清单</span>
                </div>
              </template>
              <div class="content">
                <el-table
                  :data="detectData"
                  border
                  style="width: 100%; flex: 1"
                >
                  <el-table-column prop="name" label="名称" align="center" />
                  <el-table-column prop="count" label="数量" align="center" />
                  <el-table-column prop="price" label="单价" align="center" />
                  <el-table-column label="操作" align="center">
                    <template #="{ row }">
                      <el-popconfirm
                        :title="`您确定当前检测项不正确需要删除吗？`"
                        width="250px"
                        icon="Delete"
                        @confirm="deleteItem(row)"
                      >
                        <template #reference>
                          <el-button
                            type="danger"
                            size="small"
                            icon="Delete"
                          ></el-button>
                        </template>
                      </el-popconfirm>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              <template #footer>
                <div class="btn-right">
                  <el-button
                    type="primary"
                    @click="startDetect"
                    :disabled="!isCameraOpen"
                  >
                    确定
                  </el-button>
                  <el-button type="primary" @click="getPay">结账</el-button>
                </div>
              </template>
            </el-card>
          </div>
          <div style="clear: both"></div>
        </div>
      </el-card>
    </div>
    <el-dialog v-model="dialogFormVisible" title="请输入会员ID" width="500">
      <el-form :model="customerId" :rules="rules" ref="formRef">
        <el-form-item label="会员ID" prop="id">
          <el-input
            v-model="customerId.id"
            placeholder="请输入会员ID, 若无会员ID可直接点击确认结账"
            autocomplete="off"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="confirm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="">
import { ElMessage } from 'element-plus'
import { ref, reactive } from 'vue'
import { reqSale } from '@/api/sale'
import { Text, ResponseData } from '@/api/sale/type.ts'

const imageSrc = ref('')
const isCameraOpen = ref(false)
let websocket: WebSocket | null = null

let detectData: any = ref([])

let txt: Text[] = [{ name: '', count: 0, price: 0 }]
const initWebSocket = () => {
  websocket = new WebSocket('ws://127.0.0.1:8000/api/yolov5/sale/')
  if (websocket) {
    websocket.onopen = () => {
      isCameraOpen.value = true
      console.log('WebSocket connection established.')
      // Start sending video stream to backend
    }
    websocket.onmessage = async (event) => {
      if (event.data == 'close') {
        console.log('服务器已关闭摄像头')
      } else {
        const data = JSON.parse(event.data)
        // console.log(data)
        const img = data.img
        txt = data.txt
        imageSrc.value = 'data:image/jpeg;base64,' + img
        // txt.forEach((item: any) => {
        //   detectData.value.push(item)
        // })
      }
    }
    websocket.onclose = () => {
      console.log('WebSocket connection closed.')
    }
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }
}

const closeCamera = () => {
  if (websocket) {
    websocket.send('close')
    websocket.close()
    websocket = null
  }
  isCameraOpen.value = false
}

// 删除检测不准项
const deleteItem = (row: any) => {
  const index = detectData.value.findIndex((item: any) => item === row)
  if (index !== -1) {
    detectData.value.splice(index, 1)
  }
}

// 点击确定开始检测
const startDetect = async () => {
  // 发请求之前，对整个表单校验,校验通过才能走下面逻辑
  txt.forEach((item: any) => {
    detectData.value.push(item)
  })
  console.log(detectData.value)
}

// 点击结账弹出对话框输入会员ID
const dialogFormVisible = ref(false)
const customerId: any = reactive({ id: '' })

let formRef = ref()
// 检查数字
const validateNumber = (_rule: any, value: any, callback: any) => {
  const numberRegex = /^[0-9]+$/
  if (!value || !numberRegex.test(value)) {
    callback(new Error('此处需要输入数字'))
  } else {
    callback()
  }
}

const rules = {
  id: [
    // { required: true, message: '账号长度至少为6位', rigger: 'change', min: 6, max: 10,},
    { trigger: 'change', validator: validateNumber },
  ],
}

// 点击结账跳转输入用户ID
const getPay = async () => {
  if (detectData.value.length == 0) {
    ElMessage({
      type: 'error',
      message: '尚未检测到任何商品，请打开摄像头检测！',
    })
  } else {
    dialogFormVisible.value = true
  }
}
// 点击确定加入数据库
const confirm = async () => {
  let param: any = {
    detectData: detectData.value,
    customerId: customerId.id,
  }
  let result: ResponseData = await reqSale(param)
  console.log(result)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '成功结账',
    })
    detectData.value = []
    dialogFormVisible.value = false
  } else {
    ElMessage({
      type: 'error',
      message: result.message,
    })
  }
}
</script>

<style scoped>
/* .box {
    padding: 10px;
  } */

.card {
  width: 100%;
}

.video-container {
  .box-img {
    float: left;
    /* height: auto; */
  }
  .box-card {
    float: right;
    width: 40%;
    height: 80vh;
    .right_bottom {
      position: fixed;
      bottom: 30px;
      right: 30px;
    }
  }
}
.content {
  /* 扩张身体的高度 */
  height: 55vh;
}
.btn-right {
  float: right;
}
</style>
