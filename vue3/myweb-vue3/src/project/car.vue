<template>

  <el-card>
    <template #header>
      <h3>配件异常检测部署平台</h3>
    </template>
    <el-row>
      <el-col :md="24">
        <div style="height: 20px"></div>
      </el-col>
      <el-col :md="9" :offset="1">
        <el-upload
          ref="uploadRef"
          class="avatar-uploader"
          action="/users/car/upload/"
          :show-file-list="false"
          :on-change="justSelect"
          :before-upload="beforeAvatarUpload"
          drag
          :data="{ data: 'car' }"
          :auto-upload="false"
          :on-success="handleSuccess"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          <el-icon v-else class="el-icon--upload" size="80"><IEpupload-filled /></el-icon>
        </el-upload>
        <el-button class="ml-3" type="success" @click="submitUpload"> 上传 </el-button>
      </el-col>
<!--      <el-col :md="6" :offset="1">-->
<!--        <div class="result-demo">-->
<!--          <img v-if="img_infer" :src="img_infer" />-->
<!--          <div v-else></div>-->
<!--        </div>-->
<!--      </el-col>-->
      <el-col :md="6" :offset="3">
        <div class="rec_res">
          <div>
            <p v-if="rec_result" center>
              {{judge?"正常零件":"缺陷零件"}}

            </p>
<!--            <p v-for="item of rec_result" :key="item">{{ item }}</p>-->
          </div>
        </div>
      </el-col>
      <el-col :md="24">
        <div style="height: 300px"></div>
      </el-col>
    </el-row>
  </el-card>
</template>

<script lang="ts" setup>
import type { UploadFile, UploadInstance, UploadProps } from 'element-plus'
import { b64toBlob } from '@/components/layout/Blob_convter'

const imageUrl = ref('')
const img_infer = ref('')
const rec_result = ref('')
const judge=ref(null)

const justSelect = (uploadFile: UploadFile) => {
  imageUrl.value = URL.createObjectURL(uploadFile.raw!)
}

const handleSuccess = (response: any) => {
  if (response.success) {
    // const blob = b64toBlob(response.content.img_data)
    console.log('不成功了')
    // img_infer.value = window.URL.createObjectURL(blob)
    rec_result.value = response
    // console.log(rec_result.value)
    if(response.isFault){
      judge.value=false
    }
    else{
      judge.value=true
    }
    // judge.value=(Math.random()>0.5)
    console.log(judge)
  } else {
    ElMessage.error(response.message)
  }
}
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}
const uploadRef = ref<UploadInstance>()

const submitUpload = () => {
  uploadRef.value!.submit()
}
</script>

<style lang="scss" scoped>
.avatar {
  width: 100%; /* 让图片宽度充满容器 */
  height: auto; /* 保持图片的原始宽高比 */
  display: block; /* 移除图片下方的间隙（如果图片是inline元素） */
  /* 可以添加更多样式，如圆角等 */
  //border-radius: 50%; /* 圆形图片 */
}
.avatar-uploader .el-upload {
  border: 3px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.el-icon--upload {
  font-size: 28px;
  color: #8c939d;
  height: 320px;
  text-align: center;
}

.result-demo {
  width: 410px;
  height: 434px;
  display: flex;
  border: 1px dashed var(--el-border-color);
  justify-content: center;
  align-items: center;
}
.result-demo img {
  width: 95%;
  height: 100%;
  display: block;
  object-fit: contain;
}
.rec_res {
  width: 410px;
  height: 434px;
  display: flex;
  border: 1px dashed var(--el-border-color);
  overflow-y: auto;
}
</style>