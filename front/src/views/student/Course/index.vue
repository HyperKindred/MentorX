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
 * 模拟章节数据
 */
const mockChapters: Chapter[] = [
  {
    id: 1,
    name: '第一章：Vue基础入门',
    content: '<h2>Vue.js 简介</h2><p>Vue.js 是一套用于构建用户界面的渐进式框架。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。</p><h3>核心特性</h3><ul><li>响应式数据绑定</li><li>组件化开发</li><li>虚拟DOM</li><li>指令系统</li></ul>'
  },
  {
    id: 2,
    name: '第二章：组件开发',
    content: '<h2>Vue组件</h2><p>组件是Vue.js最强大的功能之一。组件可以扩展HTML元素，封装可重用的代码。</p><h3>组件基础</h3><ul><li>组件注册</li><li>Props传递</li><li>事件通信</li><li>插槽使用</li></ul>'
  },
  {
    id: 3,
    name: '第三章：状态管理',
    content: '<h2>Vuex状态管理</h2><p>Vuex是一个专为Vue.js应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态。</p><h3>核心概念</h3><ul><li>State</li><li>Getters</li><li>Mutations</li><li>Actions</li></ul>'
  },
  {
    id: 4,
    name: '第四章：路由配置',
    content: '<h2>Vue Router</h2><p>Vue Router是Vue.js官方的路由管理器。它和Vue.js的核心深度集成，让构建单页面应用变得易如反掌。</p><h3>主要功能</h3><ul><li>嵌套的路由/视图表</li><li>模块化的、基于组件的路由配置</li><li>路由参数、查询、通配符</li><li>导航守卫</li></ul>'
  }
];


// 当前选中章节的课件内容
const currentCourseware = computed(() => {
  if (activeChapter.value === null) return null;
  const chapter = chapters.value.find(c => c.id === activeChapter.value);
  return chapter ? { title: chapter.name, content: chapter.content } : null;
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
        tabTitle = '习题练习';
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

const getChapterList = async (courseId: number) => {
  try {
    const response = await axios.post(`${store.ip}/api/getChapterList`, { id: courseId }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 5000
    });
    if (response.data.ret === 0 && response.data.chapterList?.chapter) {
      chapters.value = Array.isArray(response.data.chapterList.chapter) ? response.data.chapterList.chapter : [response.data.chapterList.chapter];
      if (chapters.value.length > 0) {
        activeChapter.value = chapters.value[0].id;
      }
    } else {
      // API返回错误时使用模拟数据
      chapters.value = mockChapters;
      activeChapter.value = mockChapters[0].id;
      ElMessage.info('已切换到模拟数据模式');
    }
  } catch (error) {
    console.error('获取章节列表失败', error);
    ElMessage.warning('网络请求失败，已切换到模拟数据模式');
    // 使用模拟数据作为后备
    chapters.value = mockChapters;
    activeChapter.value = mockChapters[0].id;
  }
};
</script>

<style scoped>
.course-page {
  display: flex;
  height: 100vh;
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
}

.courseware-body h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 24px 0 12px 0;
}

.courseware-body p {
  margin: 12px 0;
  text-align: justify;
}

.courseware-body ul {
  margin: 12px 0;
  padding-left: 24px;
}

.courseware-body li {
  margin: 6px 0;
}

.empty-content,
.placeholder-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}
</style>