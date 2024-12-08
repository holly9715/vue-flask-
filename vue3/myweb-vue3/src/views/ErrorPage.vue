<script setup lang="ts"></script>

<template>
  <div>错误</div>
  <div class="full-screen-image">
    <img src="@/assets/error.jpg" />
  </div>
</template>

<style lang="scss" scoped>
.full-screen-image {
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
