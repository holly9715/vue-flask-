<template>
  <el-card>
    <template #header>
      <h3>库存共享平台</h3>
    </template>
    <el-row>
      <div class="container">
        <div>


          <Inventory-form :columns="columns"/>

        </div>

        <div class="right-content">
          <el-input v-model="search" size="small" placeholder="Type to search"/>
          <el-button :icon="Search" circle/>
        </div>
      </div>

    </el-row>
    <el-row>
      <el-table :data="tableData" height="580" style="width: 100%">
        <el-table-column
        v-for="(column, index) in columns"
        :key="index"
        :prop="column"
        :label="column"
        :width="100"
        > </el-table-column>
        <el-table-column fixed="right" label="Operations" min-width="120">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="stockDelete(row.id.toString())">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </el-card>
</template>

<script setup>
import {Search} from '@element-plus/icons-vue'
import {computed, ref,reactive,onMounted} from 'vue'
import {getPartData} from "../api/part_inventory";
import {getAll} from "../api/menus";
import InventoryForm from "../components/inventoryForm.vue";
import request from '@/utils/request'

const columns=ref(null)
const tableData = ref(null)

// console.log(columns)
const search = ref('')
// const filterTableData = computed(() =>
//   tableData.filter(
//     (data) =>
//       !search.value ||
//       data.name.toLowerCase().includes(search.value.toLowerCase())
//   )
// )
onMounted(()=>{
  fetchData()
})
 const fetchData = async ()=> {
      try {
        const response = await getPartData();
        // console.log(response)
        // 假设后端返回的数据结构为 { columns: [{ prop: 'name', label: 'Name' }, ...], data: [...] }
        columns.value = response.data.columns;
        // console.log(columns)
        tableData.value = response.data.data;
        // console.log(tableData)
        // console.log([{'laji':2,zhende:4},{'zhen':4,'jiush':6}])
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
const handleEdit = (index, row) => {

}


const stockDelete = (id) => {
  // 确认删除
  console.log(typeof id)
  confirmDelete(id).then((confirmed) => {
    if (confirmed) {
      request({
        method:'DELETE',
        url:`/users/part_inventory/data/${id}`

      }).then(response=>{
        // console.log(response.data.success)
        if(response.data.success==true){
          ElMessage('删除成功')
            console.log('删除成功:', response.data);
          fetchData()
          // 可以在这里刷新数据列表或其他操作
        }
        else{
          ElMessage('删除失败')
        }
      })

    }
  });
};

// 显示确认删除对话框
const confirmDelete = (row) => {
  return new Promise((resolve) => {
    ElMessageBox.confirm('此操作将永久删除该文件, 是否继续?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      resolve(true);
    }).catch(() => {
      resolve(false);
    });
  });
};

</script>

<style lang="scss" scoped>
//.el-card{
//  height: 100%;
//}
.container {
  display: flex;
  justify-content: space-between; /* 在主轴上分配额外空间，使元素之间的间隔相等 */
  align-items: center; /* 在交叉轴上对齐元素 */
  width: 100%;
}

.right-content {
  display: flex; /* 使输入框和按钮在同一行 */
  align-items: center; /* 垂直居中 */
}

.right-content > :nth-child(2) {
  margin-left: 10px;
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
  height: 80%;
  display: block;
  object-fit: contain;
}
.rec_res {
  width: 410px;
  height: 434px;
  display: flex;
  border: 1px dashed var(--el-border-color);
}
</style>