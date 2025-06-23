<template>
  <div class="ai-assistant-page">
    <!-- 左侧面板 -->
    <div class="left-panel">
      <!-- 顶部章节信息 -->
      <div class="chapter-header">
        <div class="current-chapter" v-if="currentChapterName">
          <i class="el-icon-document"></i>
          <span class="chapter-name">{{ currentChapterName }}</span>
        </div>
        <div class="chapter-selector">
          <el-select
            v-model="activeChapter" 
            placeholder="选择章节"
            @change="onChapterChange"
            size="small"
          >
            <el-option
              v-for="chapter in chapters"
              :key="chapter.id"
              :label="chapter.name"
              :value="chapter.id"
            />
          </el-select>
        </div>
      </div>
      
      <!-- 历史对话列表 -->
      <div class="conversation-history">
        <div class="history-header">
          <span class="history-title">历史对话</span>
          <el-button 
            type="text" 
            size="small" 
            @click="startNewConversation"
            class="new-chat-btn"
          >
            <i class="el-icon-plus"></i>
            新对话
          </el-button>
        </div>
        <div class="history-list">
          <div 
            v-for="conversation in conversationList" 
            :key="conversation.id"
            class="conversation-item"
            :class="{ active: activeConversation === conversation.id }"
            @click="selectConversation(conversation)"
          >
            <div class="conversation-preview">
              <div class="conversation-title">{{ conversation.title || '新对话' }}</div>
              <div class="conversation-time">{{ formatTime(conversation.time) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 右侧聊天面板 -->
    <div class="right-panel">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="chat-title">
          <i class="el-icon-chat-dot-round"></i>
          <span>AI 助手</span>
        </div>
      </div>
      
      <!-- 聊天内容区域 -->
      <div class="chat-content">
        <div class="message-list" ref="messageList">
          <div v-if="messages.length === 0" class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-text">开始与AI助手对话吧！</div>
          </div>
          <div v-for="message in messages" :key="message.id" class="message-item" :class="message.sender">
            <div class="message-avatar">
              <div v-if="message.sender === 'user'" class="user-avatar">你</div>
              <div v-else class="bot-avatar">AI</div>
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              <div class="message-time">{{ formatMessageTime(message.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="chat-input-area">
        <div class="input-container">
          <el-input
            v-model="newMessage"
            type="textarea"
            :rows="1"
            :autosize="{ minRows: 1, maxRows: 4 }"
            placeholder="输入你的问题..."
            @keydown.enter.exact.prevent="sendMessage"
            @keydown.enter.shift.exact="handleShiftEnter"
            class="message-input"
          />
          <el-button 
            type="primary" 
            @click="sendMessage"
            :disabled="!newMessage.trim()"
            class="send-button"
          >
            <i class="el-icon-position"></i>
          </el-button>
        </div>
        <div class="input-hint">
          按 Enter 发送，Shift + Enter 换行
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';

/**
 * 章节接口定义
 */
interface Chapter {
  id: number;
  name: string;
}

/**
 * 课程信息接口定义
 */
interface CourseInfo {
  id: number;
  name: string;
  teacher_name: string;
}

/**
 * 消息接口定义
 */
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp?: number;
}

/**
 * 对话记录接口定义
 */
interface Conversation {
  id: number;
  title: string;
  time: number;
  chapterId: number;
}

const store = mainStore();
const courseInfo = ref<CourseInfo | null>(null);
const chapters = ref<Chapter[]>([]);
const activeChapter = ref<number | null>(null);
const messages = ref<Message[]>([]);
const newMessage = ref('');
const conversationList = ref<Conversation[]>([]);
const activeConversation = ref<number | null>(null);
const messageList = ref<HTMLElement>();

/**
 * 当前章节名称计算属性
 */
const currentChapterName = computed(() => {
  if (!activeChapter.value) return '';
  const chapter = chapters.value.find(c => c.id === activeChapter.value);
  return chapter?.name || '';
});

onMounted(() => {
  const storedCourse = localStorage.getItem('currentCourse');
  if (storedCourse) {
    courseInfo.value = JSON.parse(storedCourse);
    if (courseInfo.value) {
      getChapterList(courseInfo.value.id);
    }
  } else {
    ElMessage.error('无法加载课程信息');
  }
});

watch(activeChapter, (newChapterId) => {
  if (newChapterId !== null) {
    getChatHistory(newChapterId);
    loadConversationHistory(newChapterId);
  }
});

watch(messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
}, { deep: true });

const getChapterList = async (courseId: number) => {
  try {
    const response = await axios.post(`${store.ip}/api/getChapterList`, { id: courseId }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (response.data.ret === 0 && response.data.chapterList?.chapter) {
      chapters.value = Array.isArray(response.data.chapterList.chapter) ? response.data.chapterList.chapter : [response.data.chapterList.chapter];
      if (chapters.value.length > 0) {
        activeChapter.value = chapters.value[0].id;
      }
    } else {
      chapters.value = [];
    }
  } catch (error) {
    console.error('获取章节列表失败', error);
    ElMessage.error('获取章节列表失败');
    chapters.value = [];
  }
};

/**
 * 获取聊天历史记录
 */
const getChatHistory = async (chapterId: number) => {
  try {
    const formData = new FormData();
    formData.append('chapter_id', chapterId.toString());
    const response = await axios.post(`${store.ip}/api/student/getAiChat`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (response.data.ret === 0 && response.data.sessions?.session) {
      const history = Array.isArray(response.data.sessions.session) ? response.data.sessions.session : [response.data.sessions.session];
      messages.value = history.flatMap((s: any) => [
        { id: s.session_id * 2 - 1, text: s.question, sender: 'user', timestamp: Date.now() },
        { id: s.session_id * 2, text: s.answer, sender: 'bot', timestamp: Date.now() }
      ]);
    } else {
      messages.value = [];
    }
  } catch (error) {
    console.error('获取聊天记录失败', error);
    ElMessage.error('获取聊天记录失败');
    messages.value = [];
  }
};

/**
 * 加载对话历史列表
 */
const loadConversationHistory = (chapterId: number) => {
  // 模拟对话历史数据，实际项目中应该从后端获取
  const stored = localStorage.getItem(`conversations_${chapterId}`);
  if (stored) {
    conversationList.value = JSON.parse(stored);
  } else {
    conversationList.value = [];
  }
  
  // 如果有对话历史，选择最新的一个
  if (conversationList.value.length > 0) {
    activeConversation.value = conversationList.value[0].id;
  }
};

/**
 * 滚动到底部
 */
const scrollToBottom = () => {
  if (messageList.value) {
    messageList.value.scrollTop = messageList.value.scrollHeight;
  }
};

/**
 * 格式化时间显示
 */
const formatTime = (timestamp: number) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  
  if (diff < 60000) {
    return '刚刚';
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`;
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`;
  } else {
    return date.toLocaleDateString();
  }
};

/**
 * 格式化消息时间
 */
const formatMessageTime = (timestamp?: number) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
};

/**
 * 章节变化处理
 */
const onChapterChange = (chapterId: number) => {
  activeChapter.value = chapterId;
};

/**
 * 开始新对话
 */
const startNewConversation = () => {
  if (!activeChapter.value) {
    ElMessage.warning('请先选择章节');
    return;
  }
  
  const newConversation: Conversation = {
    id: Date.now(),
    title: '新对话',
    time: Date.now(),
    chapterId: activeChapter.value
  };
  
  conversationList.value.unshift(newConversation);
  activeConversation.value = newConversation.id;
  messages.value = [];
  
  // 保存到本地存储
  localStorage.setItem(`conversations_${activeChapter.value}`, JSON.stringify(conversationList.value));
};

/**
 * 选择对话
 */
const selectConversation = (conversation: Conversation) => {
  activeConversation.value = conversation.id;
  // 这里可以加载特定对话的消息历史
  // 目前简化处理，直接加载当前章节的所有消息
  getChatHistory(conversation.chapterId);
};

/**
 * 发送消息
 */
const sendMessage = async () => {
  if (!newMessage.value.trim() || activeChapter.value === null) return;

  const userMessage: Message = {
    id: Date.now(),
    text: newMessage.value,
    sender: 'user',
    timestamp: Date.now()
  };
  messages.value.push(userMessage);

  const question = newMessage.value;
  newMessage.value = '';

  // 如果是新对话的第一条消息，更新对话标题
  if (activeConversation.value && conversationList.value.length > 0) {
    const conversation = conversationList.value.find(c => c.id === activeConversation.value);
    if (conversation && conversation.title === '新对话') {
      conversation.title = question.length > 20 ? question.substring(0, 20) + '...' : question;
      localStorage.setItem(`conversations_${activeChapter.value}`, JSON.stringify(conversationList.value));
    }
  }

  try {
    const formData = new FormData();
    formData.append('ChapterNo', activeChapter.value.toString());
    formData.append('question', question);

    const response = await axios.post(`${store.ip}/api/student/AIchat`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (response.data.ret === 0) {
      const botMessage: Message = {
        id: Date.now() + 1,
        text: response.data.ans,
        sender: 'bot',
        timestamp: Date.now()
      };
      messages.value.push(botMessage);
    } else {
      ElMessage.error(response.data.msg || 'AI助手出错了');
    }
  } catch (error) {
    console.error('发送消息失败', error);
    ElMessage.error('发送消息失败');
  }
};

/**
 * 处理Shift+Enter换行
 */
const handleShiftEnter = (event: KeyboardEvent) => {
  // Shift+Enter时允许换行，不发送消息
  return;
};

</script>

<style scoped>
/* 主容器样式 */
.ai-assistant-page {
  display: flex;
  height: 100vh;
  background-color: #fafafa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 左侧面板样式 */
.left-panel {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

/* 章节头部样式 */
.chapter-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.current-chapter {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #374151;
  font-weight: 500;
}

.current-chapter i {
  margin-right: 8px;
  color: #6b7280;
}

.chapter-name {
  font-size: 14px;
}

.chapter-selector {
  width: 100%;
}

.chapter-selector :deep(.el-select) {
  width: 100%;
}

/* 对话历史样式 */
.conversation-history {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.history-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.new-chat-btn {
  font-size: 12px;
  color: #6366f1;
  padding: 4px 8px;
}

.new-chat-btn:hover {
  background-color: #f3f4f6;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-item {
  padding: 12px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.conversation-item:hover {
  background-color: #f9fafb;
  border-color: #e5e7eb;
}

.conversation-item.active {
  background-color: #eff6ff;
  border-color: #3b82f6;
}

.conversation-preview {
  display: flex;
  flex-direction: column;
}

.conversation-title {
  font-size: 13px;
  color: #374151;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-time {
  font-size: 11px;
  color: #9ca3af;
}

/* 右侧聊天面板样式 */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

/* 聊天头部样式 */
.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.chat-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.chat-title i {
  margin-right: 8px;
  color: #6366f1;
}

/* 聊天内容区域样式 */
.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #9ca3af;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
}

/* 消息项样式 */
.message-item {
  display: flex;
  margin-bottom: 24px;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  margin: 0 12px;
}

.user-avatar,
.bot-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.bot-avatar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.message-content {
  flex: 1;
  max-width: calc(100% - 80px);
}

.message-text {
  background: #f9fafb;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  color: #374151;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message-item.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
  text-align: right;
}

.message-item.user .message-time {
  text-align: left;
}

/* 输入区域样式 */
.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #ffffff;
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.message-input {
  flex: 1;
}

.message-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  box-shadow: none;
}

.message-input :deep(.el-textarea__inner):focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.send-button {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  padding: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.send-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  transform: none;
  box-shadow: none;
}

.input-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 8px;
  text-align: center;
}

/* 滚动条样式 */
.history-list::-webkit-scrollbar,
.message-list::-webkit-scrollbar {
  width: 4px;
}

.history-list::-webkit-scrollbar-track,
.message-list::-webkit-scrollbar-track {
  background: transparent;
}

.history-list::-webkit-scrollbar-thumb,
.message-list::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.history-list::-webkit-scrollbar-thumb:hover,
.message-list::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .left-panel {
    width: 240px;
  }
  
  .message-list {
    padding: 16px;
  }
  
  .chat-input-area {
    padding: 12px 16px;
  }
}
</style>