<template>
  <div class="course-page">
    <!-- 左侧面板 -->
    <div class="left-panel">
      <!-- 课程信息 -->
      <div class="course-header" v-if="courseInfo">
        <h2 class="course-name">{{ courseInfo.name }}</h2>
        <p class="course-teacher">讲师：{{ courseInfo.teacher_name }}</p>
      </div>
      
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
      <!-- 横向导航栏 -->
      <div class="top-navigation">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="课件" name="courseware"></el-tab-pane>
          <el-tab-pane label="习题" name="exercises"></el-tab-pane>
          <el-tab-pane label="个人练习" name="practice"></el-tab-pane>
          <el-tab-pane label="AI助手" name="ai-assistant"></el-tab-pane>
        </el-tabs>
      </div>
      
      <!-- 内容展示区域 -->
      <div class="content-area">
        <div v-if="activeTab === 'courseware'" class="courseware-content">
          <div v-if="currentCourseware" class="courseware-display">
            <h3 class="content-title">{{ currentCourseware.title }}</h3>
            <div class="courseware-body" v-html="currentCourseware.content"></div>
          </div>
          <div v-else class="empty-content">
            <el-empty description="暂无课件内容" />
          </div>
        </div>
        
        <div v-else class="placeholder-content">
          <el-empty :description="getPlaceholderText()" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import MarkdownIt from 'markdown-it';
import Exercises from '../Exercises/index.vue';
import Practice from '../Practice/index.vue';
import AiAssistant from '../AiAssistant/index.vue';

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
const activeTab = ref('courseware');
const activeChapter = ref<number | null>(null);
const courseInfo = ref<CourseInfo | null>(null);
const chapters = ref<Chapter[]>([]);

/**
 * Markdown渲染器实例
 */
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
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
  const renderedContent = chapter.content ? md.render(chapter.content) : '';
  
  return { 
    title: chapter.name, 
    content: renderedContent 
  };
});

// 选择章节
const selectChapter = (chapter: Chapter) => {
  activeChapter.value = chapter.id;
  // 切换章节时自动回到课件标签
  activeTab.value = 'courseware';
};

// 处理标签页点击
const handleTabClick = (tab: any) => {
  const tabName = tab.props.name;
  
  if (tabName !== 'courseware') {
    let tabTitle = '';
    let component: any = null;

    switch (tabName) {
      case 'exercises':
        tabTitle = '习题';
        component = Exercises;
        break;
      case 'practice':
        tabTitle = '个人练习';
        component = Practice;
        break;
      case 'ai-assistant':
        tabTitle = 'AI助手';
        component = AiAssistant;
        break;
    }
    
    if (tabTitle && component) {
      store.addTab(tabTitle, component);
      // 切换回课件，避免在当前页面显示空内容
      activeTab.value = 'courseware';
    }
  }
};

// 获取占位符文本
const getPlaceholderText = () => {
  switch (activeTab.value) {
    case 'exercises':
      return '习题功能开发中...';
    case 'practice':
      return '个人练习功能开发中...';
    case 'ai-assistant':
      return 'AI助手功能开发中...';
    default:
      return '内容加载中...';
  }
};

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
  background-color: #f5f7fa;
}

/* 左侧面板 */
.left-panel {
  width: 300px;
  background: white;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.course-header {
  padding: 24px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.course-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.course-teacher {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
}

.chapter-navigation {
  flex: 1;
  overflow-y: auto;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  padding: 20px 20px 16px 20px;
}

.chapter-list {
  padding: 0 12px 20px 12px;
}

.chapter-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.chapter-item:hover {
  background-color: #f8f9fa;
  border-color: #e4e7ed;
}

.chapter-item.active {
  background-color: #e8f4fd;
  border-color: #409eff;
  color: #409eff;
}

.chapter-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #f0f2f5;
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
  background: white;
}

.top-navigation {
  border-bottom: 1px solid #e4e7ed;
  padding: 0 24px;
}

.top-navigation :deep(.el-tabs__header) {
  margin: 0;
}

.top-navigation :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.courseware-content {
  max-width: 800px;
}

.content-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 24px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #e4e7ed;
}

.courseware-body {
  line-height: 1.6;
  color: #5a6c7d;
  font-size: 14px;
}

/* Markdown渲染内容样式 */
.courseware-body h1 {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #e4e7ed;
}

.courseware-body h2 {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 28px 0 14px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid #e4e7ed;
}

.courseware-body h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 24px 0 12px 0;
}

.courseware-body h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 20px 0 10px 0;
}

.courseware-body h5 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 18px 0 8px 0;
}

.courseware-body h6 {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin: 16px 0 6px 0;
}

.courseware-body p {
  margin: 12px 0;
  text-align: justify;
  line-height: 1.7;
}

.courseware-body ul,
.courseware-body ol {
  margin: 12px 0;
  padding-left: 24px;
}

.courseware-body li {
  margin: 6px 0;
  line-height: 1.6;
}

.courseware-body blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-left: 4px solid #409eff;
  color: #5a6c7d;
  font-style: italic;
}

.courseware-body code {
  background-color: #f1f2f6;
  color: #e74c3c;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.courseware-body pre {
  background-color: #2d3748;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 16px 0;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
}

.courseware-body pre code {
  background: none;
  color: inherit;
  padding: 0;
  border-radius: 0;
}

.courseware-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 13px;
}

.courseware-body th,
.courseware-body td {
  border: 1px solid #e4e7ed;
  padding: 8px 12px;
  text-align: left;
}

.courseware-body th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.courseware-body a {
  color: #409eff;
  text-decoration: none;
}

.courseware-body a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.courseware-body img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 12px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.courseware-body hr {
  border: none;
  border-top: 1px solid #e4e7ed;
  margin: 24px 0;
}

.courseware-body strong {
  font-weight: 600;
  color: #2c3e50;
}

.courseware-body em {
  font-style: italic;
  color: #5a6c7d;
}

.empty-content,
.placeholder-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}
</style>