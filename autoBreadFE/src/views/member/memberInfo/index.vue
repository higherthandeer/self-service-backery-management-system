<template>
  <el-card>
    <el-descriptions class="margin-top" title="会员信息" :column="1" border>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">ID</div>
        </template>
        {{ memberInfo.id }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">用户名</div>
        </template>
        {{ memberInfo.username }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">真实姓名</div>
        </template>
        {{ memberInfo.name }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">等级</div>
        </template>
        <span>{{ level[memberInfo.level] }}</span>
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">积分</div>
        </template>
        {{ memberInfo.score }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">所享折扣</div>
        </template>
        {{ memberInfo.discount }}
      </el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { reqMemberInfo } from '@/api/member'
import { Member } from '@/api/member/type'
let memberInfo: any = ref({
  id: 0,
  username: '',
  name: '',
  level: 0,
  discount: 10,
  score: 0,
})
let level: any = {
  0: '普通会员',
  1: '一级会员',
  2: '二级会员',
  3: '三级会员',
}
const getMemberInfo = async () => {
  let result: Member = await reqMemberInfo()
  // console.log(result) // 调试用可注释
  console.log(result)
  if (result.code == 200) {
    // 存储用户信息总数
    memberInfo.value = result.data

    // console.log(userParams)
  }
}
// 组件挂载完毕则发请求
onMounted(() => {
  getMemberInfo()
})
</script>

<style scoped>
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
}

.margin-top {
  margin-top: 10px;
}
</style>
