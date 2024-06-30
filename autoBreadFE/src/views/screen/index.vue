<template>
  <div class="box">
    <div class="card">
      <el-card>
        <template #header>
          欢迎来到智能入库平台
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
                  <span>检测项</span>
                </div>
              </template>
              <div class="content">
                <div style="padding-bottom: 10px">
                  请选择当前批次生产日期：
                  <el-form :model="dateParams" :rules="dateRules" ref="dateRef">
                    <el-form-item prop="date">
                      <el-date-picker
                        v-model="dateParams.date"
                        type="date"
                        placeholder="选择日期时间"
                        value-format="YYYY-MM-DD"
                      ></el-date-picker>
                    </el-form-item>
                  </el-form>
                </div>
                <el-table :data="detectData" border>
                  <el-table-column prop="name" label="名称" align="center" />

                  <el-table-column prop="count" label="数量" align="center" />

                  <el-table-column label="保质期" align="center">
                    <template #="{ row }">
                      <el-input
                        placeholder="请输入保质期"
                        v-model.number="row.shield_life"
                      ></el-input>
                    </template>
                  </el-table-column>

                  <el-table-column label="进价" align="center">
                    <template #="{ row }">
                      <el-input
                        placeholder="请输入进价"
                        v-model.number="row.price"
                      ></el-input>
                    </template>
                  </el-table-column>

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
                  <el-button type="primary" @click="startDetect">
                    确定
                  </el-button>
                  <el-button type="primary" @click="addInv">入库</el-button>
                </div>
              </template>
              <!-- <div class="right_bottom">
                <el-button type="primary" @click="confirm">确定</el-button>
              </div> -->
            </el-card>
          </div>
          <div style="clear: both"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup name="">
import { ElMessage } from 'element-plus'
import { ref, reactive } from 'vue'
import { reqAddInv } from '@/api/screen'
import { Text } from '@/api/screen/type.ts'

const imageSrc = ref('')
const isCameraOpen = ref(false)
let websocket: WebSocket | null = null
let dateParams = reactive({
  date: '',
})

// let tableParams = reactive({
//   shield_life: '',
//   price: 0,
// })
// 获
// let date = ref<string>('')

let detectData: any = ref([])

let txt: Text[] = [{ name: '', count: 0, shield_life: 0, price: 0 }]
const initWebSocket = async () => {
  await dateRef.value.validate()
  websocket = new WebSocket('ws://127.0.0.1:8000/api/yolov5/detect/')
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
        const img = data.img
        txt = data.txt
        imageSrc.value = 'data:image/jpeg;base64,' + img
        // txt.forEach((item: any) => {
        //   item['MFG_date'] = dateParams.date
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
  await dateRef.value.validate()
  txt.forEach((item: any) => {
    item['MFG_date'] = dateParams.date
    detectData.value.push(item)
  })
  console.log(detectData.value)
}

// 点击入库加入数据库
const addInv = async () => {
  let result = await reqAddInv(detectData.value)
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '入库成功',
    })
    // 检测成功后数据清空
    detectData.value = []
    dateParams.date = ''
  }
}

// 获取el-form组件实例
let dateRef = ref()

// 日期校验
// 表单校验规则对象
const dateRules: Partial<Record<string, any>> = {
  // required表明是必须字段，trigger:校验时机blur:失去焦点,change:文本变化
  date: [{ required: true, message: '请输入生产日期', trigger: 'blur' }],
}

// // 对价格类型为浮点数自定义校验规则
// const validatePrice = (_rule: any, value: any, callback: any) => {
//   const priceRegex = /^\d+(\.\d{1,2})?$/
//   if (!priceRegex.test(value)) {
//     callback(new Error('请输入正确的价格，最多保留两位小数'))
//   } else {
//     callback()
//   }
// }
// // 检查数字
// const validateNumber = (_rule: any, value: any, callback: any) => {
//   const numberRegex = /^[0-9]+$/
//   if (!value || !numberRegex.test(value)) {
//     callback(new Error('此处需要输入数字'))
//   } else {
//     callback()
//   }
// }

// // 保质期和进价校验
// const tableRules: Partial<Record<string, any>> = {
//   // required表明是必须字段，trigger:校验时机blur:失去焦点,change:文本变化
//   price: [
//     { required: true, message: '请输入单价', trigger: 'blur' },
//     {
//       validator: validatePrice,
//       trigger: 'blur',
//     },
//   ],
//   sheld_life: [
//     { required: true, message: '请输入保质期(天)', trigger: 'blur' },
//     { validator: validateNumber, trigger: 'blur' },
//   ],
// }
</script>

<style scoped>
/* .box {
  padding: 10px;
} */

.card {
  width: 100%;
}

.video-container {
  /* display: flex; */
  /* justify-content: flex-end; */
  /* justify-content: center; */
  /* align-items: center; */
  /* height: 80vh; 调整为视频的实际高度 */
  .box-img {
    float: left;
    /* height: auto; */
  }
  .box-card {
    float: right;
    width: 40%;
    height: 80vh;
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
