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
      <!-- 内容展示区域 -->
      <div class="content-area">
        <div v-if="loading" class="loading-state">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="exercises.length === 0" class="empty-state">
          <el-empty description="暂无习题"></el-empty>
        </div>
        <div v-else-if="!selectedExercise">
          <div class="exercise-list">
            <div v-for="exercise in exercises" :key="exercise.exercise_id" class="exercise-item" @click="selectExercise(exercise)">
              <div class="exercise-content">{{ exercise.exercise_content }}</div>
              <div class="exercise-meta">
                <span>类型: {{ exercise.type }}</span>
                <span>难度: {{ exercise.difficulty }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="exercise-detail">
          <el-button @click="backToList" class="back-button">返回列表</el-button>
          <h3>{{ selectedExercise.exercise_content }}</h3>
          <p><strong>类型:</strong> {{ selectedExercise.type }}</p>
          <p><strong>难度:</strong> {{ selectedExercise.difficulty }}</p>
          <!-- 这里可以添加更多习题详情，例如选项、答案等 -->
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';

interface Chapter {
  id: number;
  name: string;
}

interface CourseInfo {
  id: number;
  name: string;
  teacher_name: string;
}

interface Exercise {
  exercise_id: number;
  type: string;
  difficulty: number;
  exercise_content: string;
  is_official: string;
}

const store = mainStore();
const courseInfo = ref<CourseInfo | null>(null);
const chapters = ref<Chapter[]>([]);
const activeChapter = ref<number | null>(null);
const exercises = ref<Exercise[]>([]);
const loading = ref(false);
const selectedExercise = ref<Exercise | null>(null);

/**
 * 模拟章节数据
 */
const mockChapters: Chapter[] = [
  { id: 1, name: '第一章：Vue基础' },
  { id: 2, name: '第二章：组件开发' },
  { id: 3, name: '第三章：状态管理' },
  { id: 4, name: '第四章：路由配置' }
];

/**
 * 模拟习题数据
 */
const mockExercises: Exercise[] = [
  {
    exercise_id: 1,
    type: 'choices',
    difficulty: 1,
    exercise_content: 'Vue.js是什么类型的框架？',
    is_official: '1'
  },
  {
    exercise_id: 2,
    type: 'blanks',
    difficulty: 2,
    exercise_content: '请填空：Vue.js使用______语法进行数据绑定',
    is_official: '1'
  },
  {
    exercise_id: 3,
    type: 'answers',
    difficulty: 3,
    exercise_content: '请简述Vue.js的生命周期钩子函数',
    is_official: '1'
  },
  {
    exercise_id: 4,
    type: 'choices',
    difficulty: 2,
    exercise_content: '下列哪个是Vue.js的核心特性？',
    is_official: '1'
  }
];

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
    getExercisesList(newChapterId);
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

const getExercisesList = async (chapterId: number) => {
  loading.value = true;
  try {
    const formData = new FormData();
    formData.append('chapter_id', chapterId.toString());
    const response = await axios.post(`${store.ip}/api/student/getExercisesList`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 5000
    });
    if (response.data.ret === 0 && response.data.exercisesList?.exercise) {
      const allExercises = Array.isArray(response.data.exercisesList.exercise) ? response.data.exercisesList.exercise : [response.data.exercisesList.exercise];
      exercises.value = allExercises.filter(ex => ex.is_official === '1');
    } else {
      // API返回错误时使用模拟数据
      exercises.value = mockExercises;
      ElMessage.info('已切换到模拟数据模式');
    }
  } catch (error) {
    console.error('获取习题列表失败', error);
    ElMessage.warning('网络请求失败，已切换到模拟数据模式');
    // 使用模拟数据作为后备
    exercises.value = mockExercises;
  } finally {
    loading.value = false;
  }
};

const selectChapter = (chapter: Chapter) => {
  activeChapter.value = chapter.id;
  selectedExercise.value = null; // 切换章节时清空选中的习题
};

const selectExercise = (exercise: Exercise) => {
  selectedExercise.value = exercise;
};

const backToList = () => {
  selectedExercise.value = null;
};

</script>

<style scoped>
.course-page {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
}

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

.exercise-item {
  background: white;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  cursor: pointer;
  transition: all 0.2s ease;
}

.exercise-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.exercise-content {
  font-size: 16px;
  margin-bottom: 12px;
}

.exercise-meta {
  font-size: 14px;
  color: #606266;
}

.exercise-meta span {
  margin-right: 16px;
}

.exercise-detail {
  padding: 24px;
}

.back-button {
  margin-bottom: 20px;
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

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.exercise-item {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.exercise-item:hover {
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.exercise-content {
  font-size: 16px;
  margin-bottom: 12px;
}

.exercise-meta {
  font-size: 14px;
  color: #909399;
  display: flex;
  gap: 16px;
}
</style>