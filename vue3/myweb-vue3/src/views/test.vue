<template>
  <div>
    <el-button type="plain" round @click="centerDialogVisible = true">
      新建
    </el-button>
    <el-dialog v-model="centerDialogVisible" title="新建库存单" width="500" center>
      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="可用库存">
          <el-input v-model="form.available_stock" placeholder="请输入可用库存" />
        </el-form-item>
        <el-form-item label="库存上限">
          <el-input v-model="form.stock_upper_limit" placeholder="请输入库存上限" />
        </el-form-item>
        <el-form-item label="库存下限">
          <el-input v-model="form.stock_lower_limit" placeholder="请输入库存下限" />
        </el-form-item>
        <el-form-item label="待检库存">
          <el-input v-model="form.pending_inspection_stock" placeholder="请输入待检库存" />
        </el-form-item>
        <el-form-item label="配件名">
          <el-input v-model="form.part_name" placeholder="请输入配件名" />
        </el-form-item>
        <el-form-item label="配件编号">
          <el-input v-model="form.part_number" placeholder="请输入配件编号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="centerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="uploadStock">创建</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

// 定义对话框的可见性
const centerDialogVisible = ref(false);

// 定义表单数据
const form = ref({
  available_stock: '',
  stock_upper_limit: '',
  stock_lower_limit: '',
  pending_inspection_stock: '',
  part_name: '',
  part_number: ''
});

// 发送表单数据的方法
const uploadStock = () => {
  axios.post('/users/part_inventory/data',JSON.stringify(form.value) )
    .then(response => {
      console.log('表单提交成功:', JSON.stringify(response.data));
      centerDialogVisible.value = false;
    })
    .catch(error => {
      console.error('表单提交失败:', error);
    });
};
</script>

<style scoped>

</style>