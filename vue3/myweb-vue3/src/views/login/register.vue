<template>


   <div class="loginbody ">
    <div class="header-title">
      云平台
      </div>
    <div class="logindata card">
      <div class="logintext">
        <h2>你好，欢迎注册</h2>
      </div>
      <div class="formdata">
        <el-form :model="form" :rules="rules" ref="formRef">
          <el-form-item prop="username">
            <el-input v-model="form.username" clearable placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              clearable
              placeholder="请输入密码"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              clearable
              placeholder="再次输入密码"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.Email" clearable placeholder="请输入邮箱"></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.company" clearable placeholder="请输入供应商/公司"></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.inviteCode" clearable placeholder="请输入邀请码"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div class="butt">
        <el-button type="primary" @click="onSubmit" :loading="isLoading">注册</el-button>
      </div>
      <div style="text-align: right;">
        <router-link to="/login" class="login-link" style="display: inline-block;color: #ff0000;">登录</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { FormInstance, FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import {register} from "../../api/users"
import { useTokenStore } from '@/stores/mytoken'

const store = useTokenStore()
const router = useRouter()
const isLoading=ref(false)
const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  Email: '',
  company:'',
  inviteCode:''
})

const passwordsMatch = computed(() => form.password === form.confirmPassword)
const rules = reactive<FormRules>({
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 6, max: 12, message: '用户名长度需要6~12位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 18, message: '密码长度需要6~18位', trigger: 'blur' }
  ]
})

const formRef = ref<FormInstance>()


const onSubmit=async () => {
  await formRef.value?.validate().catch((err: any) => {
    ElMessage.error('表单校验失败...')
    isLoading.value = false
    throw err
  })
  if (!passwordsMatch.value) {
    // console.log("密码验证")
    alert('两次密码不一致！');
    return;
  }
  // console.log("1,faqingqiu")
  const data = await register(form).then((res) => {
    //这个函数好像只能返回成功
    if (!res.data.success) {
      // console.log("zhuce,faqingqiu")
      ElMessage.error('该用户名已经被注册！')
      isLoading.value = false
      throw new Error('该用户名已经被注册！')
    }
    return res.data
  })

  // store.saveToken(data.content)报错

  isLoading.value = false

  ElMessage.success('注册成功,请登录！')
  router.push('/login')

  // if (store.token.identity == '超级管理员' && store.token.username == 'vegemo-bear') {
  //   router.push('/')
  // } else {
  //   router.push('/user_look_index')
  // }
}

</script>

<style lang="scss" scoped>
.header-title {
  position: absolute; /* 设置为绝对定位 */
  top: 0; /* 顶部距离 */
  left: 10%; /* 左侧距离 */
  transform: translateX(-50%); /* 水平居中 */
  text-align: center; /* 使文本水平居中 */
  color:yellow;
  font-size: 36px; /* 设置字体大小 */
   font-family: "SimSun", sans-serif;
  margin: 20px 0; /* 设置上下外边距 */
   /* 设置背景色 */
  padding: 10px 0; /* 设置内边距 */
}

.loginbody {
    display: flex;
    justify-content: flex-end; /* 将内容推向右侧 */
    align-items: center; /* 垂直居中（如果需要的话） */
    height: 100vh; /* 假设你希望卡片垂直居中 */
    padding-right: 50px; /* 根据需要调整间距 */
}
.card {
    margin-top: -250px;
    //margin-bottom: -20;
    background-color: rgba(173, 216, 230, 0.5); /* 卡片背景色 */
    border-radius: 8px; /* 圆角 */
    box-shadow: 0 2px 12px rgba(0,0,0,0.1); /* 阴影效果 */
    width: 300px; /* 卡片宽度 */
    //height: 300px;
    padding: 20px; /* 内边距 */
    position: relative; /* 如果需要定位子元素 */
}



.loginbody {
  width: 100%;
  height: 100%;
  min-width: 1000px;
  //background-image: url('../../assets/back_ground.jpg');
  //background-size: 100% 100%;
  //background-position: center center;
  overflow: auto;
  background-repeat: no-repeat;
  position: fixed;
  line-height: 100%;
  padding-top: 150px;
}

.loginbody::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../../assets/back_ground.jpg');
  background-size: 100% 100%;
  background-position: center center;
  opacity: 1; /* 设置背景图片的透明度 */
  z-index: -1; /* 确保伪元素在内容之下 */
}

.logintext {
  margin-bottom: 20px;
  line-height: 50px;
  text-align: center;
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}

.logindata {
  width: 400px;
  height: 300px;
  transform: translate(-50%);
  margin-left: 50%;
}

.butt {
  margin-top: 10px;
  text-align: center;
}

.shou {
  cursor: pointer;
  color: #606266;
}
</style>