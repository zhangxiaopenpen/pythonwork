<template>
  <div class="chat-container">
    <div class="chat-header">
      <img src="@/assets/bg.jpg" alt="Avatar" class="avatar">
      <div class="chat-title">对话</div>
    </div>
    <div class="chat-body">
      <div class="message">
        <img src="@/assets/bg.jpg" alt="Avatar" class="avatar">
        <div class="message-content">
          请问有什么能够帮到您？
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input type="text" placeholder="输入消息..." v-model="newMessage">
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newMessage: ''
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        // 这里你可以添加发送消息的逻辑
        console.log(this.newMessage);
        this.newMessage = '';
      }
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  width: 300px;
  height: 500px;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  background-color: #fff;
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.chat-title {
  margin-left: 10px;
  font-size: 18px;
  font-weight: bold;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.message {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.message-content {
  margin-left: 10px;
  padding: 10px;
  background-color: #e0e0e0;
  border-radius: 10px;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #f5f5f5;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #0056b3;
}
</style>
