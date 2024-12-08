<template>
  <div class="loginbody">
    <div class="logindata card">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "loginFather"
}
</script>

<style scoped>
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
    background-color: rgba(173, 216, 230, 0.1); /* 卡片背景色 */
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