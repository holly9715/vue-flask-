<template>

  <el-button type="plain" round @click="centerDialogVisible = true">
            新建
  </el-button>
  <el-dialog v-model="centerDialogVisible" title="新建库存单" width="500"  center>
    <div>
      <el-form :model="form" label-width="auto" style="max-width: 600px">
<!--                v-if不行，v-show行-->
        <el-form-item v-for="(item, index) in columns" :key="index" :label="item"  v-show="index !== 0 && index !== columns.length - 1" >
      <el-input v-model="form[item]"  />
    </el-form-item>

      </el-form>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="centerDialogVisible = false;uploadStock() ">
          创建
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref,reactive} from "vue";
import request from '@/utils/request';
//
const centerDialogVisible = ref(false)
//在html中可直接使用名子，scipts中则需要props.columns
const props = defineProps(['columns'])
// console.log('a')
// console.log(props)


// do not use same name with ref
const form = ref({
})

const uploadStock=()=> {

  const response=request({
    method: 'POST',
    url: '/users/part_inventory/data',
    data: form.value,
    transformRequest: [function (data) {
    // Do whatever you want to transform the data
    let ret = ''
    for (let it in data) {
      ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
    }
    return ret
  }],
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  }).then((response)=>{
    if(response.success=true){
      ElMessage('提交表单成功')}

      else{
        ElMessage('提交表单失败')
    }
  })
}
const onSubmit = () => {
  console.log('submit!')
}
</script>

<style scoped>


</style>