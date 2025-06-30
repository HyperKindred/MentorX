<template>
  <div class="ai-assistant-page">
    <!-- 左侧面板 -->
    <div class="left-panel">
      <!-- 顶部章节信息 -->
      <div class="chapter-header">
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
                class="message-text markdown-content" 
                v-else-if="message.isTyping"
                v-html="marked.parse(message.displayText || '')"
              ></div>
              <div 
                class="message-text markdown-content" 
                v-else
                v-html="marked.parse(message.displayText || message.text)"
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
import { ref, reactive, onMounted, watch, computed, nextTick, onActivated } from 'vue';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import { ChatDotRound } from '@element-plus/icons-vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { marked } from 'marked';

/**
 * 配置marked选项
 */
marked.setOptions({
  gfm: true,
  breaks: true,
  sanitize: false
});

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

/**
 * 组件Props定义
 */
interface Props {
  courseData?: CourseInfo;
  chapterData?: Chapter[];
  activeChapterId?: number | null;
}

const props = withDefaults(defineProps<Props>(), {
  courseData: undefined,
  chapterData: () => [],
  activeChapterId: null
});

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

/**
 * 初始化课程数据
 * 优先使用props传递的课程数据，然后回退到localStorage
 */
const initCourseData = () => {
  let newCourseInfo: CourseInfo | null = null;
  
  // 优先使用props传递的课程数据
  if (props.courseData) {
    newCourseInfo = props.courseData;
  } else {
    // 回退到localStorage
    const storedCourse = localStorage.getItem('currentCourse');
    if (storedCourse) {
      newCourseInfo = JSON.parse(storedCourse);
    }
  }
  
  if (newCourseInfo) {
    // 检查是否需要更新课程数据
    if (!courseInfo.value || courseInfo.value.id !== newCourseInfo.id) {
      courseInfo.value = newCourseInfo;
      
      // 如果有传递章节数据，直接使用
      if (props.chapterData && props.chapterData.length > 0) {
        chapters.value = props.chapterData;
        // 设置激活的章节
        if (props.activeChapterId) {
          activeChapter.value = props.activeChapterId;
        } else if (chapters.value.length > 0) {
          activeChapter.value = chapters.value[0].id;
        }
      } else {
        // 没有章节数据时，重新获取
        getChapterList(newCourseInfo.id);
      }
    }
  } else {
    ElMessage.error('无法加载课程信息');
  }
};

/**
 * 组件首次挂载时初始化课程数据
 */
onMounted(() => {
  initCourseData();
});

/**
 * keep-alive组件激活时检查并更新课程数据
 */
onActivated(() => {
  initCourseData();
});

/**
 * 监听courseData props变化，当传入新的课程数据时更新组件状态
 */
watch(
  () => props.courseData,
  (newCourseData) => {
    if (newCourseData && (!courseInfo.value || courseInfo.value.id !== newCourseData.id)) {
      initCourseData();
    }
  },
  { immediate: false }
);

/**
 * 监听chapterData props变化
 */
watch(
  () => props.chapterData,
  (newChapterData) => {
    if (newChapterData && newChapterData.length > 0) {
      chapters.value = newChapterData;
      if (props.activeChapterId) {
        activeChapter.value = props.activeChapterId;
      } else if (chapters.value.length > 0) {
        activeChapter.value = chapters.value[0].id;
      }
    }
  },
  { immediate: false }
);

/**
 * 监听activeChapterId props变化
 */
watch(
  () => props.activeChapterId,
  (newActiveChapterId) => {
    if (newActiveChapterId && newActiveChapterId !== activeChapter.value) {
      activeChapter.value = newActiveChapterId;
    }
  },
  { immediate: false }
);

watch(activeChapter, (newChapterId) => {
  if (newChapterId !== null) {
    // 只调用loadConversationHistory，避免重复调用getChatHistory
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
      
      // 记录是否需要特殊处理activeConversation为-1的情况
      const shouldUpdateActiveConversation = activeConversation.value === -1;
      
      // 如果activeConversation为-1，说明是新对话，需要设置为最新的session_id
      if (shouldUpdateActiveConversation && sessions.length > 0) {
        // 找到最新的session_id（时间最晚的）
        const latestSession = sessions.reduce((latest: any, current: any) => {
          return new Date(current.time).getTime() > new Date(latest.time).getTime() ? current : latest;
        });
        activeConversation.value = latestSession.session_id;
      }
      
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
            time: new Date(s.time + ' +08:00').getTime(), // 后端返回北京时间，明确指定时区
            chapterId: chapterId
          });

        }
      });
      
      // 更新对话列表，按时间倒序排列
      conversationList.value = Array.from(conversationMap.values()).sort((a, b) => b.time - a.time);
      
      // 如果是从activeConversation为-1的状态更新过来的，只更新左侧列表，不更新右侧消息
      if (shouldUpdateActiveConversation) {
        // 只更新左侧对话列表，保持右侧当前消息不变
        return;
      }
      
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
              timestamp: new Date(s.time + ' +08:00').getTime() // 后端返回北京时间，明确指定时区
            }));
          } else if (s.type === 'A') {
            messageList.push(reactive<Message>({
              id: messageId++,
              text: s.content,
              sender: 'bot',
              timestamp: new Date(s.time + ' +08:00').getTime() // 后端返回北京时间，明确指定时区
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
  
  // 注意：不再自动清空当前对话状态，保持用户当前的对话不变
  // 只有在明确开始新对话时才清空
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
      typewriterEffect(botMessage, response.data.answer, 15);
      
      // 如果是新对话且成功，先设置临时ID并重新获取历史对话列表
      if (isNewConversation && activeChapter.value) {
        // 设置临时ID为-1，表示需要在getChatHistory中设置为最新对话
        activeConversation.value = -1;
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
 * 逐字显示文本效果（随机速度模拟AI思考）
 * @param message - 要显示的消息对象
 * @param fullText - 完整的文本内容
 * @param baseSpeed - 基础显示速度（毫秒），默认30ms
 */
const typewriterEffect = (message: Message, fullText: string, baseSpeed: number = 30) => {
  let index = 0;
  
  // 确保响应式更新
  message.displayText = '';
  message.isTyping = true;
  message.text = fullText; // 先设置完整文本
  
  /**
   * 递归函数，为每个字符设置随机延迟
   */
  const typeNextChar = () => {
    if (index < fullText.length) {
      message.displayText = fullText.substring(0, index + 1);
      index++;
      
      // 自动滚动到底部
      nextTick(() => {
        scrollToBottom();
      });
      
      // 生成随机延迟时间：基础速度 ± 50%的随机变化
      // 对于标点符号和空格，增加额外的停顿时间
      const currentChar = fullText[index - 1];
      let randomDelay = baseSpeed + Math.random() * baseSpeed - baseSpeed / 2;
      
      // 标点符号后增加停顿，模拟AI思考
      if (/[。！？；，、：]/.test(currentChar)) {
        randomDelay += Math.random() * 25 + 10; // 额外50-150ms停顿
      } else if (/[\s\n]/.test(currentChar)) {
        randomDelay += Math.random() * 25 + 10; // 空格和换行增加10-35ms停顿
      }
      
      // 确保延迟时间不小于10ms
      randomDelay = Math.max(10, randomDelay);
      
      setTimeout(typeNextChar, randomDelay);
    } else {
      message.isTyping = false;
    }
  };
  
  // 开始打字效果
  typeNextChar();
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
  background-color: transparent;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 左侧面板样式 */
.left-panel {
  width: 280px;
  background: var(--backgroundColor2);
  border-right: 2px solid var(--backgroundColor);
  display: flex;
  flex-direction: column;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

/* 章节头部样式 */
.chapter-header {
  padding: 16px;
  border-bottom: 2px solid var(--backgroundColor);
  background: var(--backgroundColor1);
}

.current-chapter {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: var(--titleColor);
  font-weight: 500;
}

.current-chapter i {
  margin-right: 8px;
  color: #6b7280;
}

.chapter-name {
  font-size: 14px;
  color: white;
}

.chapter-selector {
  width: 100%;

}

.chapter-selector :deep(.el-select) {
  width: 100%;
}

.el-icon-document {
  height: 1.8rem;
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
  border-bottom: 2px solid var(--backgroundColor);
}

.history-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--titleColor);
}

.new-chat-btn {
  font-size: 12px;
  color: var(--textColor2);
  padding: 4px 8px;
}

.new-chat-btn:hover {
  color: var(--textColor);
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
  background-color: var(--titleColor2);
}

.conversation-item.active {
  background-color: var(--borderColor);
  border-color: #3b82f6;
}

.conversation-preview {
  display: flex;
  flex-direction: column;
}

.conversation-title {
  font-size: 13px;
  color: var(--textColor);
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
  background: transparent;
}



/* 聊天头部样式 */
.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--backgroundColor);
  background: var(--backgroundColor2);
}

.chat-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
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
  margin: 0 12px;
}

.message-item.user .message-content {
  margin-left: 68px;
  margin-right: 12px;
  width: fit-content;
  max-width: none;
  flex: none;
}

.message-item.bot .message-content {
  max-width: calc(100% - 80px);
  margin-left: 12px;
  margin-right: 68px;
}

.message-text {
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
  background: var(--titleColor2);
  padding: 20px;
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--textColor);
}

.message-item.user .message-text {
  background: var(--titleColor2);
  padding: 10px 20px;
  text-align: left;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  line-height: 1.7;
  color: var(--textColor);
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





/* 输入区域样式 */
.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid var(--backgroundColor);
  background: var(--backgroundColor2);
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  align-items: center;
}

.message-input {
  flex: 1;
}

.message-input :deep(.el-textarea__inner) {
  border-radius: 12px;
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