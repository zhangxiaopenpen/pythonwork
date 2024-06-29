<template>
  <div class="chat-container">
    <div class="chat-body custom-scrollbar">
      <div v-for="(message, index) in messages" :key="index" :class="['message-container','content', message.sender]">
        <div v-if="message.sender === 'bot'" class="avatar bot-avatar"></div>
        <div :class="['message', message.sender]">{{ message.text }}</div>
        <div v-if="message.sender === 'user'" class="avatar user-avatar"></div>
      </div>
    </div>
    <div class="parent-container">
      <div class="input-container">
        <input type="text" v-model="userMessage" @keyup.enter="sendMessage" class="custom-input" placeholder="请输入您的问题">
        <div class="voice-icon-container" @click="audioCHangeWord" @mouseover="changeImage" @mouseleave="restoreImage">
          <img :src="imageUrl" alt="" class="voice-icon">
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      userMessage: '',
      messages: [],
      imageUrl: 'assets/语音(gray).png',
      newImageUrl: 'assets/语音(black).png',
      originalImageUrl: 'assets/语音(gray).png',
      listenImageUrl: 'assets/声波.png',
      word: "",
      isListening: false, // 判断是否在语音监听中
    };
  },
  mounted() {
    // 自动发送初始消息
    this.messages.push({ text: '请问有什么能帮到您？', sender: 'bot' });
  },
  methods: {
    sendMessage() {
      if (this.userMessage.trim() !== '') {
        this.messages.push({ text: this.userMessage, sender: 'user' });
        this.sendMessageToServer(this.userMessage)
        this.userMessage = '';
      }
    },
    changeImage() {
      if(this.imageUrl==this.listenImageUrl){
        return;
      }
      this.imageUrl = this.newImageUrl; // 鼠标悬浮时改变图片地址
    },
    restoreImage() {
      if(this.imageUrl==this.listenImageUrl){
        return;
      }
      this.imageUrl = this.originalImageUrl; // 鼠标移开时恢复原始图片地址
    },
    audioCHangeWord() {
      var that = this;
      that.word = "";
      // 创建SpeechRecognition对象
      // eslint-disable-next-line no-undef
      var recognition = new webkitSpeechRecognition();
      console.log("recognition1", recognition);
      if (!recognition) {
        // eslint-disable-next-line no-undef
        recognition = new SpeechRecognition();
      }
      console.log("recognition2", recognition);
      console.log(11);
      // 设置语言
      recognition.lang = 'zh-CN';
      console.log(22);
      // 开始语音识别
      recognition.start();
      that.isListening = true;
      this.imageUrl = this.listenImageUrl;
      console.log(33);
      // 监听识别结果
      recognition.onresult = function (event) {
        var result = event.results[0][0].transcript;
        console.log("监听结果:", result);
        that.word = result;
      };

      // 监听错误事件
      recognition.onerror = function (event) {
        that.isListening = false;
        console.error(event.error);
      };
      // 监听结束事件（包括识别成功、识别错误和用户停止）
      recognition.onend = () => {
        that.isListening = false;
        console.log("语音识别停止");
        this.messages.push({ text: this.word, sender: 'user' });
        this.sendMessageToServer(this.word)
        this.word = ""
        this.imageUrl = this.originalImageUrl;

      };

    },
    //消息发送给后端并获得结果
    async sendMessageToServer(msg){
      // Simulate a response from the bot
      // setTimeout(() => {
      //   this.messages.push({ text: '自动回复', sender: 'bot' });
      // }, 1000);
      
      try {
        const response = await axios.post('http://127.0.0.1:6006/chat'/** 'https://api.example.com/data'*/
            ,{msg:msg});
        const result = response.data.message;
        this.messages.push({ text: result, sender: 'bot' });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
          
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  width: 800px;
  height: 100%;
  /** background-color: #f0fcfc; */
  background-color: rgba(0, 0, 0, 0);
  border-radius: 10px;
  /** box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); **/
  overflow: hidden;

}

.chat-header {
  display: flex;
  align-items: center;
  background-color: #ffe4e1;
  padding: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  background-size: cover;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.bot-avatar {
  background-image: url('@/assets/avater-bot.png'); /* Replace with your bot avatar image path */
}

.user-avatar {
  background-image: url('@/assets/avater-user.jpg'); /* Replace with your user avatar image path */
  order: 2;
}


.chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  margin-top: 30px;
}

.chat-input input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chat-input button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #ff7f7f;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.parent-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  margin-bottom: 55px;
}

.input-container {
  border-radius: 20px; /* 设置输入框两端的弧度 */
  background-color: white; /* 输入框的背景色 */
  display: flex;
  width: 750px; /* 输入框的宽度 */
  height: 80px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}


.custom-input {
  margin-left: 10px;
  width: calc(100% - 40px); /* 输入框宽度减去左边框和语音图标的宽度 */
  padding: 10px;
  border: none;
  border-radius: 20px; /* 设置输入框两端的弧度 */
  background-color: white; /* 输入框的背景色 */
  outline: none; /* 去除默认的选中边框 */
  font-size: 20px;
}

/*.custom-input:focus {
  border: 2px solid #6d95c9; !* 设置选中状态下的边框样式 *!
}*/

.voice-icon-container {
  margin-right: 10px;
}

.voice-icon {
  height: 30px; /* 调整语音图标的高度 */
  margin-top:20px;
}

.message-container {
  display: flex;
  /*align-items: center;*/
  margin: 5px 0;
}

.message-container.user {
  justify-content: flex-end;
}

.message-container.bot {
  justify-content: flex-start;
}

.message {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  margin: 0 10px;
  color: #181818;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.message.user {
  background-color: #b9e2e8;
  order: 1;
}

.message.bot {
  background-color: #b9e2e8;
}
/* Style for the scrollbar container */
.custom-scrollbar {
  height: 300px; /* Customize as needed */
  width: 100%; /* Customize as needed */
  overflow-y: auto; /* Enable vertical scrollbar */
  scrollbar-width: thin; /* Thin scrollbar */
  scrollbar-color: rgba(220, 233, 233, 0.5) rgba(255, 255, 255, 0.1); /* Scrollbar color */
  border-radius: 20px;
}

/* Custom scrollbar styles */
/* For WebKit browsers */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px; /* Customize as needed */
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(155, 155, 155, 0.5); /* Customize as needed */
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(155, 155, 155, 0.7); /* Customize as needed */
}

/* Add more styles as needed for your content */
.content {
  /* Your content styles */
}
</style>





