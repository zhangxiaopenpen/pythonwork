<template>
  <div id="app" class="app-container">
    <ChatBox />
  </div>
</template>

<script>
import ChatBox from './components/ChatBox.vue';
export default {
  name: 'App',
  components: {
    ChatBox
  }
};
</script>
<style>
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 高度100% */
  margin: 0;
}

body, html {
  height: 100%;
  margin: 0;

  background-image: url('@/assets/bg.jpg');
  background-size: cover; /* 使背景图像覆盖整个区域 */
  background-repeat: no-repeat; /* 防止背景图像重复 */
  background-position: center; /* 将背景图像置于中心 */
}
</style>
