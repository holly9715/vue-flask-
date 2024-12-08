<script setup lang="ts">
import { isCollapse } from './isCollapse'
</script>

<template>
  <el-aside>
    <el-scrollbar>
      <el-menu router :collapse="isCollapse" background-color="#545c64">
        <a href="/" class="logo">
          <img src="@/assets/平台logo.jpg" />
          <h1>模拟云平台</h1>
        </a>
        <el-menu-item index="/">
          <el-icon> <IEpMonitor /></el-icon><span> 工作台 </span>
        </el-menu-item>
        <el-menu-item index="/user_menu">
          <el-icon><IEpLock /></el-icon> <span> 用户管理 </span>
        </el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <el-icon style="color: white"> <IEpPromotion /> </el-icon>
            <span style="color: white"> 项目管理 </span>
          </template>
          <el-menu-item index="/cooperate">
            <el-icon><IEpPear /></el-icon> <span> 供应链协同 </span>
          </el-menu-item>
          <el-menu-item index="/share">
            <el-icon><IEpGrape /></el-icon> <span> 数据安全共享 </span>
          </el-menu-item>
          <el-menu-item index="/fl">
            <el-icon><IEpGrape /></el-icon> <span> 联邦学习 </span>
          </el-menu-item>
          <el-menu-item index="/car">
            <el-icon><IEpGrape /></el-icon> <span> 汽车配件异常检测 </span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </el-aside>
</template>

<style lang="scss" scoped>
.el-aside {
  background-color: #545c64;
  height: 100vh;
  width: auto;
}
.el-menu {
  border-right: none;
  width: 200px;
  &.el-menu--collapse {
    width: 60px;
    & h1 {
      display: none;
    }
  }
  .el-menu-item {
    color: white;
  }
}
.logo {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  text-decoration: none;
  color: white;
  background-color: #545c64;
  img {
    width: 32px;
    height: 32px;
  }
}
</style>
