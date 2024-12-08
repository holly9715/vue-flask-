<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const HandleOCR = () => {
  router.push('/cooperate')
}
const HandleLPDR = () => {
  router.push('/share')
}
const HandleCar=()=>{
  router.push('/car')
}
const HandleFL=()=>{
  router.push('/fl')
}
</script>

<template>
  <el-row>
    <el-col :md="4" :offset="1">
      <div class="container">
        <img src="@/assets/库存.jpg" />
        <div class="content">
          <h5 class="proj">供应链协同</h5>
          <p class="desc">对供应链下的物流进行记录和管理</p>
          <el-button type="primary" @click="HandleOCR">

            <el-icon><IEpPromotion /></el-icon>
            <span>进入</span>
          </el-button>
        </div>
      </div>
    </el-col>
    <el-col :md="4" :offset="1">
      <div class="container">
        <img src="@/assets/数据共享.jpg" />
        <div class="content">
          <h5 class="proj">数据安全共享</h5>
          <p class="desc">公共数据分享库，实现数据共享，企业共赢</p>
          <el-button type="primary" @click="HandleLPDR">
            <el-icon><IEpPromotion /></el-icon>
            <span>进入</span>
          </el-button>
        </div>
      </div>
    </el-col>
    <el-col :md="4" :offset="1">
      <div class="container">
        <img src="@/assets/数据共享2.jpg" />
        <div class="content">
          <h5 class="proj">联邦学习</h5>
          <p class="desc">模型文件下载，上传的联邦学习训练流程</p>
          <el-button type="primary" @click="HandleFL">
            <el-icon><IEpPromotion /></el-icon>
            <span>进入</span>
          </el-button>
        </div>
      </div>
    </el-col>
    <el-col :md="4" :offset="1">
      <div class="container">
        <img src="@/assets/汽车配件.jpg" />
        <div class="content">
          <h5 class="proj">汽车配件异常检测</h5>
          <p class="desc">对汽车配件的缺陷进行识别检测</p>
          <el-button type="primary" @click="HandleCar">
            <el-icon><IEpPromotion /></el-icon>
            <span>进入</span>
          </el-button>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<style lang="scss" scoped>
.container {
  padding-top: 0px;
  width: 280px;
  height: 360px;
  display: flex;
  flex-direction: column;
  outline: 1px dashed #ccc;
  justify-content: center;
  align-items: center;
  border-top: 1px dashed #ccc;
}

img {
  width: 90%;
  height: 90%;
  padding-top: 5px;
}

.content {
  padding-left: 0px;
  padding-top: 10px;
  padding-bottom: 5px;
}

.proj {
  font-size: 20px;
  padding-bottom: 8px;
}
.desc {
  font-size: 15px;
  padding-bottom: 8px;
}
</style>
