<template>
  <div class="chat">
    <h2>Простой чат</h2>

    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" class="message">
        {{ msg }}
      </div>
    </div>

    <form @submit.prevent="sendMessage">
      <input
        v-model="newMessage"
        placeholder="Введите сообщение"
        class="input"
      />
      <button type="submit" class="button">Отправить</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,             // WebSocket-соединение
      messages: [],         // Список сообщений
      newMessage: '',       // Сообщение из input
    };
  },
  mounted() {
    // Подключаемся к серверу WebSocket
    this.ws = new WebSocket('ws://localhost:8000/ws');

    // Получаем сообщения от сервера
    this.ws.onmessage = (event) => {
      this.messages.push(event.data);
    };

    this.ws.onopen = () => {
      console.log('WebSocket подключен');
    };

    this.ws.onclose = () => {
      console.log('WebSocket отключен');
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        this.ws.send(this.newMessage);     // Отправляем сообщение
        this.newMessage = '';              // Очищаем поле
      }
    },
  },
};
</script>

<style scoped>
.chat {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.messages {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
  border: 1px solid #eee;
  padding: 10px;
  background: #f9f9f9;
}

.message {
  padding: 5px;
  border-bottom: 1px solid #ddd;
}

.input {
  width: 70%;
  padding: 8px;
}

.button {
  padding: 8px 12px;
  margin-left: 5px;
}
</style>
