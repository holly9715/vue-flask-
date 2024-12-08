<template>
  <el-card style="height:100%">
    <template #header>
      <h3>联邦学习训练平台</h3>
    </template>
    <el-container style="display: flex; flex-direction: column; height: 100%">
      <el-row style="margin-bottom: 20px;">
        <el-upload
          ref="upload"
          class="upload-demo"
          action="/users/fl/uploadModel"
          :limit="1"
          :on-exceed="handleExceed"
          :auto-upload="false"
          accept=".pkl, .pt, .pth"
        >
          <template #trigger>
            <el-button type="primary" round>选择文件</el-button>
          </template>
          <el-button class="ml-3" style="margin-left: 25px;" type="success" @click="submitUpload" round>
            上传至服务器
          </el-button>
          <template #tip>
            <div class="el-upload__tip text-red">
              limit 1 file, new file will cover the old file
            </div>
          </template>
        </el-upload>
      </el-row>

      <el-row>
        <el-button  type="success" @click="submitDownload" round>
          下载文件
        </el-button>
      </el-row>


      <el-row v-if="downloadStatusVisible" style="margin-top: 0px;">
        <ul class="el-upload-list el-upload-list--text">
          <li class="el-upload-list__item is-ready" tabindex="0">
            <div class="el-upload-list__item-info">
              <a class="el-upload-list__item-name">
                <i class="el-icon el-icon--document">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                    <path fill="currentColor" d="M832 384H576V128H192v768h640V384zm-26.496-64L640 154.496V320h165.504zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32zm160 448h384v64H320v-64zm0-192h160v64H320v-64zm0 384h384v64H320v-64z"/>
                  </svg>
                </i>
                <span class="el-upload-list__item-file-name">{{ downloadStatusText }}</span>
              </a>
            </div>
            <label class="el-upload-list__item-status-label">
              <i class="el-icon el-icon--upload-success el-icon--circle-check">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                  <path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768zm0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896z"/>
                  <path fill="currentColor" d="M745.344 361.344a32 32 0 0 1 45.312 45.312l-288 288a32 32 0 0 1-45.312 0l-160-160a32 32 0 1 1 45.312-45.312L480 626.752l265.344-265.408z"/>
                </svg>
              </i>
            </label>

            <i class="el-icon--close-tip">press delete to remove</i>
          </li>
        </ul>
      </el-row>

    </el-container>
  </el-card>
</template>

<script lang="ts" setup>
import {Upload,Download} from '@element-plus/icons-vue'
import { ref } from 'vue'
import { genFileId } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import request from "@/utils/request";
import {downloadModel, getModel, getPartData} from "@/api/part_inventory";

const fileType=['pkl','pt','pth']
const upload = ref<UploadInstance>()
const downloadStatusVisible = ref(true);
const downloadStatusText = ref('x235');

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

onMounted(async ()=>{
try {
        const response = await getModel();
        downloadStatusText.value = response.data.filename;

      } catch (error) {
        console.error('Error fetching data:', error);
      }
})
const submitDownload=async ()=>{
  try {
        const response = await downloadModel();
        // downloadStatusText.value = response.data.filename;
    console.log(response)
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download',downloadStatusText.value); // 设置 download 属性
    document.body.appendChild(link);
    link.click(); // 触发点击事件下载文件
    document.body.removeChild(link); // 清理
    URL.revokeObjectURL(url); // 释放 URL 对象
      } catch (error) {
        console.error('Error fetching data:', error);
      }
}
const submitUpload = () => {
  upload.value!.submit()
}
</script>

<style scoped>
.el-card {
  height: 100%;
}

.el-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.ml-3 {
  margin-left: 25px;
}

.el-upload-list {
  list-style: none;
  padding: 0;
  margin-top: 20px;
}

.el-upload-list__item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  margin-bottom: 8px;
  width: 100%; /* 确保宽度与上传组件一致 */
}

.el-upload-list__item-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.el-upload-list__item-name {
  display: flex;
  align-items: center;
  color: var(--el-text-color-primary);
}

.el-upload-list__item-file-name {
  margin-left: 8px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.el-upload-list__item-status-label {
  margin-left: 8px;
}

.el-icon {
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: middle;
  fill: currentColor;
  overflow: hidden;
}

/* Element Plus 图标 */
.el-icon-document:before {
  content: "\E6D4";
  font-family: element-icons;
}

.el-icon-circle-check:before {
  content: "\E6C8";
  font-family: element-icons;
}

.el-icon-close:before {
  content: "\E6C7";
  font-family: element-icons;
}

.el-icon--close-tip {
  display: none;
}
</style>