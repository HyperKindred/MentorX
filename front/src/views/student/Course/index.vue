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
import { marked } from 'marked';
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
  text-align: left;
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

/* 课件内容 Markdown 样式 - Typora风格 */
.courseware-body {
  line-height: 1.7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  color: #2c3e50;
}

/* 标题样式 */
.courseware-body h1,
.courseware-body h2,
.courseware-body h3,
.courseware-body h4,
.courseware-body h5,
.courseware-body h6 {
  margin: 24px 0 16px 0;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
}

.courseware-body h1 {
  font-size: 2em;
  border-bottom: 2px solid #eaecef;
  padding-bottom: 12px;
  margin-bottom: 20px;
}

.courseware-body h2 {
  font-size: 1.6em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.courseware-body h3 {
  font-size: 1.3em;
}

.courseware-body h4 {
  font-size: 1.1em;
}

.courseware-body h5 {
  font-size: 1em;
}

.courseware-body h6 {
  font-size: 0.9em;
  color: #6a737d;
}

/* 段落样式 */
.courseware-body p {
  margin: 16px 0;
  text-align: justify;
  text-justify: inter-ideograph;
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

/* 引用样式 */
.courseware-body blockquote {
  border-left: 4px solid #dfe2e5;
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  background-color: #f8f9fa;
  border-radius: 0 3px 3px 0;
}

.courseware-body blockquote p {
  margin: 12px 0;
}

/* 行内代码样式 */
.courseware-body code {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 3px;
  padding: 2px 6px;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', monospace;
  font-size: 0.85em;
  color: #d73a49;
}

/* 代码块样式 */
.courseware-body pre {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  font-size: 0.85em;
  line-height: 1.45;
}

.courseware-body pre code {
  background: none;
  border: none;
  padding: 0;
  color: #24292e;
  font-size: inherit;
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

.empty-content,
.placeholder-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}
</style>