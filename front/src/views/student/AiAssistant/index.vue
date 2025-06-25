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
              <div class="message-text" v-if="message.sender === 'user'">{{ message.text }}</div>
              <div 
                class="message-text" 
                v-else-if="message.isTyping"
              >
                <span class="typing-text">{{ message.displayText }}</span>
                <span class="typing-cursor">|</span>
              </div>
              <div 
                class="message-text markdown-content" 
                v-else
                v-html="marked(message.displayText || message.text)"
              ></div>
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
            :disabled="!newMessage.trim() || isLoading"
            :loading="isLoading"
            class="send-button"
          >
            <i class="el-icon-position" v-if="!isLoading"></i>
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
import { ref, reactive, onMounted, watch, computed, nextTick } from 'vue';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { marked } from 'marked';

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
  isTyping?: boolean;
  displayText?: string;
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
const isLoading = ref(false);

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
    const formData = new FormData();
    formData.append('id', courseId.toString());
    const response = await axios.post(`${store.ip}/api/getChapterList`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.data.ret === 0 && response.data.chapterList) {
      chapters.value = Array.isArray(response.data.chapterList) ? response.data.chapterList : [response.data.chapterList];
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

    if (response.data.ret === 0 && response.data.sessions) {
      const sessions = Array.isArray(response.data.sessions) ? response.data.sessions : [response.data.sessions];
      
      // 构建对话列表，按session_id分组
      const conversationMap = new Map<number, Conversation>();
      const questionsMap = new Map<number, string>(); // 存储每个session的第一个问题
      
      sessions.forEach((s: any) => {
        if (!conversationMap.has(s.session_id)) {
          // 查找该session的第一个问题作为标题
          const firstQuestion = sessions.find((item: any) => item.session_id === s.session_id && item.type === 'Q');
          const title = firstQuestion ? 
            (firstQuestion.content.length > 20 ? firstQuestion.content.substring(0, 20) + '...' : firstQuestion.content) :
            s.session_name || '默认对话';
            
          conversationMap.set(s.session_id, {
            id: s.session_id,
            title: title,
            time: new Date(s.time).getTime(), // 使用API返回的时间
            chapterId: chapterId
          });
        }
      });
      
      // 更新对话列表，按时间倒序排列
      conversationList.value = Array.from(conversationMap.values()).sort((a, b) => b.time - a.time);
      
      // 如果当前没有选择对话，则不显示任何消息
      if (activeConversation.value === null) {
        messages.value = [];
      } else {
        // 如果选择了对话，显示该对话的消息
        const selectedSessions = sessions.filter((s: any) => s.session_id === activeConversation.value);
        
        // 按时间排序并构建消息列表
        const sortedSessions = selectedSessions.sort((a: any, b: any) => new Date(a.time).getTime() - new Date(b.time).getTime());
        
        const messageList: Message[] = [];
        let messageId = 1;
        
        sortedSessions.forEach((s: any) => {
          if (s.type === 'Q') {
            messageList.push(reactive<Message>({
              id: messageId++,
              text: s.content,
              sender: 'user',
              timestamp: new Date(s.time).getTime()
            }));
          } else if (s.type === 'A') {
            messageList.push(reactive<Message>({
              id: messageId++,
              text: s.content,
              sender: 'bot',
              timestamp: new Date(s.time).getTime()
            }));
          }
        });
        
        messages.value = messageList;
      }
    } else {
      conversationList.value = [];
      messages.value = [];
    }
  } catch (error) {
    console.error('获取聊天记录失败', error);
    ElMessage.error('获取聊天记录失败');
    conversationList.value = [];
    messages.value = [];
  }
};

/**
 * 加载对话历史列表
 */
const loadConversationHistory = (chapterId: number) => {
  // 重新获取历史对话列表
  getChatHistory(chapterId);
  
  // 默认不选择任何对话，进入新对话模式
  activeConversation.value = null;
  messages.value = [];
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
  
  // 清空当前选择，进入新对话模式
  activeConversation.value = null;
  messages.value = [];
};

/**
 * 选择对话
 */
const selectConversation = (conversation: Conversation) => {
  activeConversation.value = conversation.id;
  // 重新获取聊天历史，这会触发getChatHistory中的逻辑来显示选中对话的消息
  getChatHistory(conversation.chapterId);
};

/**
 * 发送消息
 */
const sendMessage = async () => {
  if (!newMessage.value.trim() || activeChapter.value === null || isLoading.value) return;

  const userMessage = reactive<Message>({
    id: Date.now(),
    text: newMessage.value,
    sender: 'user',
    timestamp: Date.now()
  });
  messages.value.push(userMessage);

  const question = newMessage.value;
  newMessage.value = '';
  
  // 记录是否为新对话
  const isNewConversation = activeConversation.value === null;
  
  // 设置加载状态
  isLoading.value = true;
  
  // 添加加载消息
  const loadingMessage = reactive<Message>({
    id: Date.now() + 1,
    text: '',
    sender: 'bot',
    timestamp: Date.now(),
    isTyping: true,
    displayText: 'AI正在思考中...'
  });
  messages.value.push(loadingMessage);

  try {
    const formData = new FormData();
    formData.append('chapter_id', activeChapter.value.toString());
    formData.append('content', question);
    
    // 如果未选择历史对话，使用session_id=-1表示新对话
    if (activeConversation.value === null) {
      formData.append('session_id', '-1');
    } else {
      formData.append('session_id', activeConversation.value.toString());
    }

    const response = await axios.post(`${store.ip}/api/student/AIchat`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (response.data.ret === 0) {
      // 移除加载消息
      messages.value.pop();
      
      // 创建AI回复消息（使用reactive确保响应式）
      const botMessage = reactive<Message>({
        id: Date.now() + 2,
        text: response.data.answer,
        sender: 'bot',
        timestamp: Date.now(),
        isTyping: true,
        displayText: ''
      });
      messages.value.push(botMessage);
      
      // 开始逐字显示效果
      typewriterEffect(botMessage, response.data.answer, 30);
      
      // 如果是新对话且成功，重新获取历史对话列表
      if (isNewConversation && activeChapter.value) {
        getChatHistory(activeChapter.value);
      }
    } else {
      // 移除加载消息
      messages.value.pop();
      ElMessage.error(response.data.msg || 'AI助手出错了');
      throw new Error(response.data.msg || 'AI助手出错了');
    }
  } catch (error) {
    // 移除加载消息
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].isTyping) {
      messages.value.pop();
    }
    console.error('发送消息失败', error);
    ElMessage.error('发送消息失败');
  } finally {
    isLoading.value = false;
  }
};

/**
 * 逐字显示文本效果
 * @param message - 要显示的消息对象
 * @param fullText - 完整的文本内容
 * @param speed - 显示速度（毫秒）
 */
const typewriterEffect = (message: Message, fullText: string, speed: number = 30) => {
  let index = 0;
  
  // 确保响应式更新
  message.displayText = '';
  message.isTyping = true;
  message.text = fullText; // 先设置完整文本
  
  const timer = setInterval(() => {
    if (index < fullText.length) {
      message.displayText = fullText.substring(0, index + 1);
      index++;
      // 自动滚动到底部
      nextTick(() => {
        scrollToBottom();
      });
    } else {
      message.isTyping = false;
      clearInterval(timer);
    }
  }, speed);
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
  height: 100%;
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

/* AI消息的Markdown内容样式优化 */
.message-text.markdown-content {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  padding: 20px;
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #2c3e50;
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

/* 打字效果样式 */
.typing-text {
  display: inline;
}

.typing-cursor {
  display: inline-block;
  animation: blink 1s infinite;
  color: #6366f1;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

/* Markdown内容样式 - Typora风格 */
.markdown-content {
  line-height: 1.7;
}

/* 标题样式 */
.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 24px 0 16px 0;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
}

.markdown-content h1 {
  font-size: 2em;
  border-bottom: 2px solid #eaecef;
  padding-bottom: 12px;
  margin-bottom: 20px;
}

.markdown-content h2 {
  font-size: 1.6em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.markdown-content h3 {
  font-size: 1.3em;
}

.markdown-content h4 {
  font-size: 1.1em;
}

.markdown-content h5 {
  font-size: 1em;
}

.markdown-content h6 {
  font-size: 0.9em;
  color: #6a737d;
}

/* 段落样式 */
.markdown-content p {
  margin: 16px 0;
  text-align: justify;
  text-justify: inter-ideograph;
}

/* 列表样式 */
.markdown-content ul,
.markdown-content ol {
  margin: 16px 0;
  padding-left: 24px;
}

.markdown-content li {
  margin: 8px 0;
  line-height: 1.6;
}

.markdown-content ul li {
  list-style-type: disc;
}

.markdown-content ol li {
  list-style-type: decimal;
}

/* 嵌套列表 */
.markdown-content ul ul,
.markdown-content ol ol,
.markdown-content ul ol,
.markdown-content ol ul {
  margin: 4px 0;
}

/* 行内代码样式 */
.markdown-content code {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 3px;
  padding: 2px 6px;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', monospace;
  font-size: 0.85em;
  color: #d73a49;
}

/* 代码块样式 */
.markdown-content pre {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  font-size: 0.85em;
  line-height: 1.45;
}

.markdown-content pre code {
  background: none;
  border: none;
  padding: 0;
  color: #24292e;
  font-size: inherit;
}

/* 引用样式 */
.markdown-content blockquote {
  border-left: 4px solid #dfe2e5;
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  background-color: #f8f9fa;
  border-radius: 0 3px 3px 0;
}

.markdown-content blockquote p {
  margin: 12px 0;
}

/* 表格样式 */
.markdown-content table {
  border-collapse: collapse;
  margin: 20px 0;
  width: 100%;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  overflow: hidden;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #d0d7de;
  padding: 12px 16px;
  text-align: left;
  vertical-align: top;
}

.markdown-content th {
  background-color: #f6f8fa;
  font-weight: 600;
  color: #24292e;
}

.markdown-content tr:nth-child(even) {
  background-color: #f6f8fa;
}

.markdown-content tr:hover {
  background-color: #f1f8ff;
}

/* 链接样式 */
.markdown-content a {
  color: #0969da;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

.markdown-content a:hover {
  color: #0550ae;
  border-bottom-color: #0969da;
}

.markdown-content a:visited {
  color: #8250df;
}

/* 强调样式 */
.markdown-content strong {
  font-weight: 600;
  color: #24292e;
}

.markdown-content em {
  font-style: italic;
  color: #656d76;
}

/* 分隔线样式 */
.markdown-content hr {
  border: none;
  height: 2px;
  background-color: #d0d7de;
  margin: 24px 0;
  border-radius: 1px;
}

/* 删除线样式 */
.markdown-content del {
  text-decoration: line-through;
  color: #656d76;
}

/* 高亮样式 */
.markdown-content mark {
  background-color: #fff8c5;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 图片样式 */
.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 任务列表样式 */
.markdown-content input[type="checkbox"] {
  margin-right: 8px;
  transform: scale(1.1);
}

.markdown-content .task-list-item {
  list-style: none;
  margin-left: -20px;
}

/* 键盘按键样式 */
.markdown-content kbd {
  background-color: #f6f8fa;
  border: 1px solid #d0d7de;
  border-bottom-color: #afb8c1;
  border-radius: 6px;
  box-shadow: inset 0 -1px 0 #afb8c1;
  color: #24292e;
  display: inline-block;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 11px;
  line-height: 10px;
  padding: 3px 5px;
  vertical-align: middle;
}

/* 脚注样式 */
.markdown-content .footnote {
  font-size: 0.8em;
  color: #656d76;
  vertical-align: super;
}

/* 数学公式样式 */
.markdown-content .math {
  font-family: "Times New Roman", serif;
  font-size: 1.1em;
}

/* 首行缩进优化 */
.markdown-content p:first-child {
  margin-top: 0;
}

.markdown-content p:last-child {
  margin-bottom: 0;
}

/* 代码语言标签 */
.markdown-content pre[class*="language-"]::before {
  content: attr(class);
  position: absolute;
  top: 8px;
  right: 12px;
  font-size: 0.75em;
  color: #656d76;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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