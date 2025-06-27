<template>
  <div class="course-page">
    <!-- 左侧面板 -->
    <div class="left-panel">   
      <!-- 章节导航 -->
      <div class="chapter-navigation">
        <h3 class="nav-title">课程章节</h3>
        <div class="chapter-list">
          <div 
            v-for="(chapter, index) in chapters" 
            :key="chapter.id"
            class="chapter-item"
            :class="{ active: activeChapter === chapter.id }"
            @click="selectChapter(chapter)"
          >
            <span class="chapter-number">{{ index + 1 }}</span>
            <span class="chapter-title">{{ chapter.name }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 右侧面板 -->
    <div class="right-panel">
      <!-- 功能按钮组 -->
      <div class="function-buttons">
        <div class="button-group">
          <el-button 
             type="primary" 
             :icon="Document" 
             class="function-btn active"
             disabled
           >
             课件学习
           </el-button>
           <el-button 
             type="default" 
             :icon="Edit" 
             class="function-btn"
             @click="openExercises"
           >
             章节习题
           </el-button>
           <el-button 
             type="default" 
             :icon="Notebook" 
             class="function-btn"
             @click="openPractice"
           >
             个人练习
           </el-button>
           <el-button 
             type="default" 
             :icon="ChatDotRound" 
             class="function-btn"
             @click="openAiAssistant"
           >
             AI助手
           </el-button>
        </div>
      </div>
      
      <!-- 内容展示区域 -->
      <div class="content-area">
        <div class="courseware-content">
          <div v-if="currentCourseware" class="courseware-display">
            <h3 class="content-title">{{ currentCourseware.title }}</h3>
            <div class="courseware-body" v-html="currentCourseware.content"></div>
          </div>
          <div v-else class="empty-content">
            <el-empty description="暂无课件内容" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onActivated, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { Document, Edit, Notebook, ChatDotRound } from '@element-plus/icons-vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { marked } from 'marked';
import Exercises from '../Exercises/index.vue';
import Practice from '../Practice/index.vue';
import AiAssistant from '../AiAssistant/index.vue';

/**
 * 组件Props定义
 */
interface Props {
  courseData?: CourseInfo;
}

const props = withDefaults(defineProps<Props>(), {
  courseData: undefined
});

interface Chapter {
  id: number;
  name: string;
  content: string;
}

interface CourseInfo {
  id: number;
  name: string;
  teacher_name: string;
}

const store = mainStore();
const activeChapter = ref<number | null>(null);
const courseInfo = ref<CourseInfo | null>(null);
const chapters = ref<Chapter[]>([]);
/**
 * Markdown渲染器实例
 */
/**
 * 配置marked选项
 */
marked.setOptions({
  gfm: true,
  breaks: true,
  sanitize: false
});




/**
 * 当前选中章节的课件内容
 * 将Markdown格式的内容渲染为HTML
 */
const currentCourseware = computed(() => {
  if (activeChapter.value === null) return null;
  const chapter = chapters.value.find(c => c.id === activeChapter.value);
  if (!chapter) return null;
  
  // 渲染Markdown内容为HTML
  const renderedContent = chapter.content ? marked.parse(chapter.content) : '';
  
  return { 
    title: chapter.name, 
    content: renderedContent 
  };
});

/**
 * 选择章节
 * @param chapter 章节对象
 */
const selectChapter = (chapter: Chapter) => {
  activeChapter.value = chapter.id;
};

/**
 * 打开习题页面
 */
const openExercises = () => {
  if (courseInfo.value && chapters.value.length > 0) {
    store.addTab('章节习题', Exercises, {
      courseData: courseInfo.value,
      chapterData: chapters.value,
      activeChapterId: activeChapter.value
    });
  } else {
    ElMessage.warning('课程信息不完整，无法跳转');
  }
};

/**
 * 打开个人练习页面
 */
const openPractice = () => {
  if (courseInfo.value && chapters.value.length > 0) {
    store.addTab('个人练习', Practice, {
      courseData: courseInfo.value,
      chapterData: chapters.value,
      activeChapterId: activeChapter.value
    });
  } else {
    ElMessage.warning('课程信息不完整，无法跳转');
  }
};

/**
 * 打开AI助手页面
 */
const openAiAssistant = () => {
  if (courseInfo.value && chapters.value.length > 0) {
    store.addTab('AI助手', AiAssistant, {
      courseData: courseInfo.value,
      chapterData: chapters.value,
      activeChapterId: activeChapter.value
    });
  } else {
    ElMessage.warning('课程信息不完整，无法跳转');
  }
};



/**
  * 初始化课程数据
  * 优先使用props传递的课程数据，然后回退到localStorage
  */
 const initCourseData = () => {
   let newCourseInfo: CourseInfo | null = null;
   
   // 优先使用props传递的课程数据
   if (props.courseData) {
     newCourseInfo = props.courseData;
   }
   
   if (newCourseInfo) {
     // 检查是否需要更新课程数据
     if (!courseInfo.value || courseInfo.value.id !== newCourseInfo.id) {
       courseInfo.value = newCourseInfo;
       getChapterList(newCourseInfo.id);
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
      courseInfo.value = newCourseData;
      getChapterList(newCourseData.id);
    }
  },
  { immediate: false }
);

/**
 * 获取课程章节列表
 * @param courseId 课程ID
 */
const getChapterList = async (courseId: number) => {
  try {
    // 使用FormData格式发送请求
    const formData = new FormData();
    formData.append('id', courseId.toString());
    
    const response = await axios.post(`${store.ip}/api/getChapterList`, formData, {
      timeout: 5000
    });
    if (response.data.ret === 0) {
      // 处理API返回的章节数据，确保chapterList是数组格式
      const chapterList = response.data.chapterList;
      if (chapterList) {
        chapters.value = Array.isArray(chapterList) ? chapterList : [chapterList];
        if (chapters.value.length > 0) {
          activeChapter.value = chapters.value[0].id;
        }
      } else {
        chapters.value = [];
      }
    } else {
      chapters.value = [];
      ElMessage.error('获取章节列表失败：' + response.data.msg);
    }
  } catch (error) {
    console.error('获取章节列表失败', error);
    ElMessage.error('网络请求失败，请稍后重试');
    chapters.value = [];
  }
};
</script>

<style scoped>
.course-page {
  display: flex;
  height: 100%;
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}

/* 左侧面板 */
.left-panel {
  width: 300px;
  background: var(--backgroundColor2);
  border-right: 1.5px solid transparent;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  display: flex;
  flex-direction: column;
}



.chapter-navigation {
  flex: 1;
  overflow-y: auto;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
  padding: 20px 20px 16px 20px;
}

.chapter-list {
  padding-bottom: 20px;
  padding-left: 5px;
  padding-right: 5px;
}

.chapter-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  border-radius: 5px;
  background-color: transparent;
  color: var(--textColor2);
}

.chapter-item:hover {
  background-color: var(--backgroundColor2);
  color: var(--titleColor);
}

.chapter-item.active {
  background-color: transparent;
  color: var(--titleColor);
  background-color: var(--backgroundColor2);
  font-weight: 540;
}

.chapter-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  margin-right: 12px;
  flex-shrink: 0;
}

.chapter-item.active .chapter-number {
  background-color: #409eff;
  color: white;
}

.chapter-title {
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

/* 右侧面板 */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* 功能按钮组样式 */
.function-buttons {
  padding: 20px 24px;
  background: transparent;
}

.button-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.function-btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 12px 20px;
  transition: all 0.3s ease;
  border: 1px solid var(--textColor2);
  background-color: var(--backgroundColor2);
  color: var(--textColor2);
}

.function-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadowColor2);
  color: var(--textColor);
  border: 1.5px solid var(--textColor);
}

.function-btn.active {
  background: #417dff;
  border-color: #409eff;
  color: white;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.4);
}

.function-btn :deep(.el-icon) {
  margin-right: 6px;
}

/* 内容区域样式优化 */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
  background: transparent;
}

.courseware-content {
  max-width: 900px;
  margin: 0 auto;
}

/* 课件展示卡片样式 */
.courseware-display {
  background-color: var(--backgroundColor3);
  border-radius: 16px;
  box-shadow: 0 4px 20px var(--shadowColor);
  overflow: hidden;
  transition: all 0.3s ease;
}

.courseware-display:hover {
  box-shadow: 0 8px 30px var(--shadowColor2);
  transform: translateY(-2px);
}

/* 课件标题样式 */
.content-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--titleColor);
  margin: 0;
  padding: 32px 32px 24px 32px;
  background: var(--backgroundColor3);
}

/* 课件内容容器 */
.courseware-body {
  padding-left: 4rem;
  padding-right: 4rem;
  padding-top: 10px;
  padding-bottom: 2rem;
  line-height: 1.8;
  color: #334155;
  font-size: 15px;
  background: var(--backgroundColor3);
}

/* 课件内容 Markdown 样式 - 现代化设计 */
.courseware-body {
  line-height: 1.8;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 15px;
  color: var(--textColor);
  text-align: left;
}

/* 标题样式优化 */
.courseware-body h1,
.courseware-body h2,
.courseware-body h3,
.courseware-body h4,
.courseware-body h5,
.courseware-body h6 {
  margin: 32px 0 20px 0;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
  letter-spacing: -0.025em;
}

.courseware-body h1 {
  font-size: 2.25em;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  border-bottom: 3px solid #e2e8f0;
  padding-bottom: 16px;
  margin-bottom: 28px;
}

.courseware-body h2 {
  font-size: 1.75em;
  color: #475569;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 12px;
  margin-bottom: 24px;
}

.courseware-body h3 {
  font-size: 1.5em;
  color: #475569;
  margin-bottom: 20px;
}

.courseware-body h4 {
  font-size: 1.25em;
  color: #64748b;
  margin-bottom: 18px;
}

.courseware-body h5 {
  font-size: 1.125em;
  color: #64748b;
  margin-bottom: 16px;
}

.courseware-body h6 {
  font-size: 1em;
  color: #94a3b8;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

/* 段落样式优化 */
.courseware-body p {
  margin: 20px 0;
  text-align: justify;
  text-justify: inter-ideograph;
  color: #475569;
  font-size: 15px;
  line-height: 1.8;
}

/* 列表样式 */
.courseware-body ul,
.courseware-body ol {
  margin: 16px 0;
  padding-left: 24px;
}

.courseware-body li {
  margin: 8px 0;
  line-height: 1.6;
}

.courseware-body ul li {
  list-style-type: disc;
}

.courseware-body ol li {
  list-style-type: decimal;
}

/* 嵌套列表 */
.courseware-body ul ul,
.courseware-body ol ol,
.courseware-body ul ol,
.courseware-body ol ul {
  margin: 4px 0;
}

/* 引用样式优化 */
.courseware-body blockquote {
  border-left: 4px solid #3b82f6;
  margin: 24px 0;
  padding: 20px 24px;
  color: #475569;
  background: #f8fafc;
  border-radius: 0 12px 12px 0;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  position: relative;
  font-style: italic;
}

.courseware-body blockquote::before {
  content: '"';
  position: absolute;
  top: 12px;
  left: -8px;
  font-size: 48px;
  color: #3b82f6;
  font-family: Georgia, serif;
  line-height: 1;
}

.courseware-body blockquote p {
  margin: 16px 0;
  font-size: 16px;
  line-height: 1.7;
}

/* 行内代码样式优化 */
.courseware-body code {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 3px 8px;
  font-family: 'JetBrains Mono', 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', monospace;
  font-size: 0.875em;
  color: #7c3aed;
  font-weight: 500;
}

/* 代码块样式优化 */
.courseware-body pre {
  background: #1e293b;
  border: 1px solid #475569;
  border-radius: 12px;
  padding: 24px;
  margin: 24px 0;
  overflow-x: auto;
  font-size: 0.875em;
  line-height: 1.6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: relative;
}

.courseware-body pre::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px 12px 0 0;
}

.courseware-body pre code {
  background: none;
  border: none;
  padding: 0;
  color: #e2e8f0;
  font-size: inherit;
  font-weight: 400;
}

/* 表格样式 */
.courseware-body table {
  border-collapse: collapse;
  margin: 20px 0;
  width: 100%;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  overflow: hidden;
}

.courseware-body th,
.courseware-body td {
  border: 1px solid #d0d7de;
  padding: 12px 16px;
  text-align: left;
  vertical-align: top;
}

.courseware-body th {
  background-color: #f6f8fa;
  font-weight: 600;
  color: #24292e;
}

.courseware-body tr:nth-child(even) {
  background-color: #f6f8fa;
}

.courseware-body tr:hover {
  background-color: #f1f8ff;
}

/* 链接样式 */
.courseware-body a {
  color: #0969da;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

.courseware-body a:hover {
  color: #0550ae;
  border-bottom-color: #0969da;
}

.courseware-body a:visited {
  color: #8250df;
}

/* 图片样式 */
.courseware-body img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 分隔线样式 */
.courseware-body hr {
  border: none;
  height: 2px;
  background-color: #d0d7de;
  margin: 24px 0;
  border-radius: 1px;
}

/* 强调样式 */
.courseware-body strong {
  font-weight: 600;
  color: #24292e;
}

.courseware-body em {
  font-style: italic;
  color: #656d76;
}

/* 删除线样式 */
.courseware-body del {
  text-decoration: line-through;
  color: #656d76;
}

/* 高亮样式 */
.courseware-body mark {
  background-color: #fff8c5;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 任务列表样式 */
.courseware-body input[type="checkbox"] {
  margin-right: 8px;
  transform: scale(1.1);
}

.courseware-body .task-list-item {
  list-style: none;
  margin-left: -20px;
}

/* 键盘按键样式 */
.courseware-body kbd {
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

/* 首行缩进优化 */
.courseware-body p:first-child {
  margin-top: 0;
}

.courseware-body p:last-child {
  margin-bottom: 0;
}

/* 空状态样式优化 */
.empty-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  margin: 0 auto;
  max-width: 900px;
}

.empty-content :deep(.el-empty) {
  padding: 60px 40px;
}

.empty-content :deep(.el-empty__image) {
  width: 120px;
  height: 120px;
}

.empty-content :deep(.el-empty__description) {
  color: #64748b;
  font-size: 16px;
  margin-top: 24px;
  font-weight: 500;
}

/* 滚动条样式 */
.chapter-navigation::-webkit-scrollbar,
.content-area::-webkit-scrollbar {
  width: 4px;
}

.chapter-navigation::-webkit-scrollbar-track,
.content-area::-webkit-scrollbar-track {
  background: transparent;
}

.chapter-navigation::-webkit-scrollbar-thumb,
.content-area::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.chapter-navigation::-webkit-scrollbar-thumb:hover,
.content-area::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .left-panel {
    width: 240px;
  }
  
  .content-area {
    padding: 16px;
  }
  
  .function-buttons {
    padding: 16px 20px;
  }
}
</style>