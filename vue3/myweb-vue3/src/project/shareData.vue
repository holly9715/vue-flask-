<template>
  <el-card>
    <template #header>
      <h3>数据文件共享平台</h3>
    </template>
    <div>
      <el-button type="primary" size="small" style="width: 70px;" plain @click="Bupload">上传</el-button>
      <el-button type="success" size="small" style="width: 70px;" plain @click="centerDialogVisible=true">新建文件夹</el-button>
      <el-button type="warning" size="small" style="width: 70px;" plain @click="Bdownload">批量下载</el-button>
      <el-button type="danger" size="small" style="width: 70px;" plain @click="Bdelete">批量删除</el-button>
    </div>
<el-dialog
    v-model="centerDialogVisible"
    title="设置文件名"
    width="500"
    align-center
    @open="handleDialogOpen"
  >
<span>文件夹名：</span>
    <el-input
      v-model="dirname"
      ref="dirnameInput"
      style="width: 240px"
      placeholder="请输入文件夹名"
      :suffix-icon="Calendar"

    />
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="BnewDir()">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
    <div>
      <el-table
          :data="tableData"
          row-key="name"
          ref="multipleTableRef"
          height="580"
          :default-sort="{ prop: 'isDir', order: 'descending' }"
          @selection-change="handleSelectionChange"
          @select="handleSelect"

      >
        <el-table-column type="selection" width="55"/>
        <el-table-column label="Name" sortable>
          <template #default="{ row }">
            <!--            TODO-->
            <el-icon v-if="row.isDir">
              <Folder/>
            </el-icon>
            <el-icon v-else>
              <Document/>
            </el-icon>

            {{ row.name }}
          </template>
        </el-table-column>
        <el-table-column prop="size" label="size"/>
        <el-table-column prop="uploadTime" label="uploadTime"/>
        <el-table-column fixed="right" label="Operations" min-width="120">
          <template #default="{row}">
            <el-button v-if="row.isDir?true:false" link type="primary" size="small" min-width="30" class="left-button"
                       @click="handleUploadClick(row)">
              上传文件

            </el-button>
            <el-button v-else="row.isDir?true:false" link type="primary" size="small" min-width="30" class="left-button"
                       @click="handleDownloadClick(row)">
              下载文件
            </el-button>
            <el-button link type="primary" size="small" class="right-button" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </el-card>
</template>

<script lang="ts" setup>
import {Document, Folder} from "@element-plus/icons-vue";
import {ref, reactive, onMounted,watch,nextTick} from 'vue'
import type Node from 'element-plus/es/components/tree/src/model/node'
import {getShareData} from "@/api/part_inventory";
import request from '@/utils/request'
import axios from "axios";
import {ElMessage, ElMessageBox} from 'element-plus'
// import {MenuItem} from "@/api/menus";

const  multipleTableRef=ref()
const dirnameInput = ref(null); // 使用 ref 引用输入框
const dirname=ref('')
const centerDialogVisible=ref(false)
const treeProps = reactive({
  checkStrictly: false,
  children: 'children',
  hasChildren: 'isDir'
})
const tableData = ref(null)
const selectedRows = ref([])

onMounted(() => {
  fetchData()
  // tableData.value=[]
})

const handleDialogOpen=()=> {
      // 在对话框打开时聚焦输入框
      nextTick(()=>{
        dirnameInput.value.focus();
        // dirnameInput.value.select();
      })
}

// console.log(tableData)

const fetchData = async () => {
  try {
    const response = await getShareData();
    tableData.value = response.data;
    // console.log(tableData.value)
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function handleDownloadClick(row) {
  // const formData = new ();
  // formData.append('file', file);
  // formData.append('path', row.path);
  console.log(row.path)
  const response = request({
    method: 'GET',
    url: `/users/share/download/${row.path}`,
    responseType: 'blob'
    // data: formData
  }).then((response) => {
    // 更新表格数据
    // fetchData();
    console.log(response.headers['content-disposition'])
    // console.log
    return response
  }).then(response => {
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'default-filename.txt'; // 默认文件名

    if (contentDisposition && contentDisposition.includes('filename=')) {
      const parts = contentDisposition.split(';');
      for (let part of parts) {
        if (part.trim().startsWith('filename=')) {
          filename = decodeURIComponent(part.split('=')[1].trim().replace(/"/g, ''));
          break;
        }
      }
    }
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename); // 设置 download 属性
    document.body.appendChild(link);
    link.click(); // 触发点击事件下载文件
    document.body.removeChild(link); // 清理
    URL.revokeObjectURL(url); // 释放 URL 对象
    fetchData()
  })
      .catch(error => {
        console.error('Error:', error);
      });

}

const handleUploadClick = (row) => {
  uploadFiles(row);
}

function handleDelete(row) {
  // 显示确认对话框
  console.log(row.path)
  ElMessageBox.confirm(`确定删除 "${row.name}"？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    // 执行删除操作
    try {
      await deleteItemFromServer(row.path);
      ElMessage.success('删除成功');
    } catch (error) {
      // 有问题
      console.log(error.message)
      // ElMessage.error('删除失败: ' + error.message);
    }
  }).catch(() => {
    ElMessage.info('已取消删除');
  });
}

async function deleteItemFromServer(path) {
  const formData = new FormData();
  // formData.append('file', file);
  formData.append('path', path);
  const response = await request({
    method: 'POST',
    url: '/users/share/delete',
    data: formData
  }).then((response) => {
    // 更新表格数据
    fetchData();
    return response
  });
  console.log(response)
  if (response.status === 200) {
    // 从 tableData 中移除该行

  }
}

const uploadFiles = (row) => {
  ElMessage.info('在文件夹' + row.name + '上传文件');
  // 创建一个隐藏的 input 文件选择器
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.style.display = 'none';

  // 将文件输入添加到 DOM
  document.body.appendChild(fileInput);

  // 触发点击事件以打开文件选择器
  fileInput.click();

  // 处理文件选择事件
  fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      handleFileUpload(files[0], row.path);
    }
  });
  // 清除文件输入以允许重新选择相同的文件
  fileInput.addEventListener('click', () => {
    fileInput.value = null;
  });
}

const handleFileUpload = (file, path) => {
  const formData = new FormData();
  // console.log(path)
  formData.append('file', file);
  formData.append('path', path); // 假设 row.id 存储父目录的 ID
  request({
    method: 'POST',
    url: '/users/share/upload',
    data: formData
  }).then((response) => {
    ElMessage.success('File uploaded successfully!');
    // 更新表格数据
    fetchData();
  }).catch((error) => {
    console.log(error)
    ElMessage.error('Failed to upload file.');
  });
}

const Bupload = () => {
  ElMessage.info('在根目录下上传文件');
  // 创建一个隐藏的 input 文件选择器
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.style.display = 'none';
  // 将文件输入添加到 DOM
  document.body.appendChild(fileInput);
  // 触发点击事件以打开文件选择器
  fileInput.click();
  // 处理文件选择事件
  fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      handleFileUpload(files[0], 'public');
    }
  });
  // 清除文件输入以允许重新选择相同的文件
  fileInput.addEventListener('click', () => {
    fileInput.value = null;
  });
}

const handleSelectionChange = (rows) => {
  selectedRows.value = rows;
  console.log('Selected rows:', rows);
};

// const handleSelect = (selection,row){
//
//   if (selection.length > 0) {
//         // 选择了或取消选择了节点'
//     let parent=[]
//     if(selection.length>selectedRows.value.length){
//       //父节点要不要选
//       selectAncestors(row);
//     }else{
//       //父节点全删
//       deleteAncestors(row);
//     }
//         updateAncestors(row);
//       }
//   selectedRows.value=selection
// }
// function selectAncestors(row){
//
// }
// function deleteAncestors(row){
//
// }

const BnewDir = () => {
  // console.log('feikong')
  // console.log(dirname)
  centerDialogVisible.value = false
  if(dirname.value){
  if (selectedRows.value.length <= 1) {
    if (selectedRows.value.length === 0) {
      // console.log('genmulu')
      request({
      method: 'GET',
      url: '/users/share/upload',
      params:{
        path:selectedRows.path?selectedRows.path:'public',
        dirname:dirname.value
      }
      // responseType:'blob'
      // data: formData
    }).then((respond) => {
      fetchData()
      ElMessage('在根目录下新建文件夹成功')
    })

  } else {
      if(selectedRows.value.isDir){
        request({
      method: 'GET',
      url: '/users/share/upload',
      params:{
        path:selectedRows.path?selectedRows.path:'public',
        dirname:dirname.value
      }
      // responseType:'blob'
      // data: formData
    }).then((respond) => {
      fetchData()
      ElMessage(`在${selectedRows.path}下新建文件夹成功`)
    })
      }
    }
    dirname.value=''
}
else
{
  ElMessage('请选择一个目录')
}

}
else{
  ElMessage('目录名不能为空')
}}

const Bdownload=()=>{
  console.log('xiazai')
  selectedRows.value.forEach((item)=>{
    if(!item.isDir){
      console.log(item.path)
      const response = request({
    method: 'GET',
    url: `/users/share/download/${item.path}`,
    responseType: 'blob'
    // data: formData
  }).then((response) => {
    // 更新表格数据
    // fetchData();
    console.log(response.headers['content-disposition'])
    // console.log
    return response
  }).then(response => {
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'default-filename.txt'; // 默认文件名

    if (contentDisposition && contentDisposition.includes('filename=')) {
      const parts = contentDisposition.split(';');
      for (let part of parts) {
        if (part.trim().startsWith('filename=')) {
          filename = decodeURIComponent(part.split('=')[1].trim().replace(/"/g, ''));
          break;
        }
      }
    }
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename); // 设置 download 属性
    document.body.appendChild(link);
    link.click(); // 触发点击事件下载文件
    document.body.removeChild(link); // 清理
    URL.revokeObjectURL(url); // 释放 URL 对象
    fetchData()
  }).catch(error => {
        console.error('Error:', error);
      });
    }
  })
}

const Bdelete=()=>{

}
</script>


<style lang="scss" scoped>
.button-container {
  //position: relative;
  //justify-content: flex-end; /* 内容右对齐 */

}

.el-button {
  width: 50px; /* 设置一个固定宽度 */
}

.left-button {
  position: absolute;
  left: 5px;
  margin-left: 0px; /* 如果需要的话，可以调整间距 */
  top: 50%;
  transform: translateY(-50%);
}

.right-button {
  position: absolute;
  left: 0;
  margin-left: 70px; /* 如果需要的话，可以调整间距 */
  top: 50%;
  transform: translateY(-50%);
}

.el-card {
  height: 100%;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.avatar-uploader .el-upload {
  border: 3px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

a {
  color: blue;
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
