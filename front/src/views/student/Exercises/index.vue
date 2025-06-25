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
              <div class="exercise-content">{{ formatExerciseContent(exercise.exercise_content, 80) }}</div>
              <div class="exercise-meta">
                <span class="exercise-type">{{ getExerciseTypeText(exercise.type) }}</span>
                <span class="exercise-difficulty">难度: {{ exercise.difficulty }}</span>
                <span class="exercise-status" :class="{ 'submitted': exercise.is_committed === 1 }">
                  {{ exercise.is_committed === 1 ? '已提交' : '未提交' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="exercise-detail">
          <el-button @click="backToList" class="back-button">返回列表</el-button>
          
          <!-- 题目区域 -->
          <div class="question-section">
            <div class="question-header">
              <h2>题目内容</h2>
              <div class="question-meta">
                <el-tag type="info">{{ getExerciseTypeText(selectedExercise.type) }}</el-tag>
                <el-tag type="warning">难度: {{ selectedExercise.difficulty }}</el-tag>
                <el-tag v-if="selectedExercise.is_committed" type="success">已提交</el-tag>
                <el-tag v-else type="danger">未提交</el-tag>
              </div>
            </div>
            <div class="question-content" v-html="marked.parse(selectedExercise.exercise_content)"></div>
          </div>
          
          <!-- 作答区域 -->
          <div class="answer-section">
            <div class="answer-header">
              <h3>{{ selectedExercise.is_committed ? '历史答题内容' : '作答区' }}</h3>
              <div v-if="selectedExercise.is_committed && selectedExercise.submitted_at" class="submit-time">
                提交时间: {{ new Date(selectedExercise.submitted_at).toLocaleString() }}
              </div>
            </div>
            
            <!-- 已提交状态：显示历史答案 -->
            <div v-if="selectedExercise.is_committed" class="submitted-answer">
              <div class="answer-content">
                <pre>{{ selectedExercise.student_answer }}</pre>
              </div>
              <div class="answer-actions">
                <el-button @click="editAnswer" type="primary" plain disabled>已提交，不可重新作答</el-button>
              </div>
            </div>
            
            <!-- 未提交状态：显示作答区 -->
            <div v-else class="answer-input">
              <el-input
                v-model="currentAnswer"
                type="textarea"
                :rows="8"
                placeholder="请在此输入您的答案..."
                maxlength="2000"
                show-word-limit
              />
              <div class="answer-actions">
                <el-button @click="submitAnswer" type="primary" :loading="submitting">
                  {{ submitting ? '提交中...' : '提交答案' }}
                </el-button>
              </div>
            </div>
            
            <!-- 重新作答状态（已移除，因为已提交的题目不允许重新作答） -->
          </div>
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
import { marked } from 'marked';

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
  is_official: number | string;
  is_committed: number;
  student_answer?: string;
  submitted_at?: string;
}

const store = mainStore();
const courseInfo = ref<CourseInfo | null>(null);
const chapters = ref<Chapter[]>([]);
const activeChapter = ref<number | null>(null);
const exercises = ref<Exercise[]>([]);
const loading = ref(false);
const selectedExercise = ref<Exercise | null>(null);
const currentAnswer = ref<string>('');
const submitting = ref(false);



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
    const formData = new FormData();
    formData.append('id', courseId.toString());

    const response = await axios.post(`${store.ip}/api/getChapterList`, formData, {
      timeout: 5000
    });
    if (response.data.ret === 0 && response.data.chapterList) {
      chapters.value = Array.isArray(response.data.chapterList) ? response.data.chapterList : [response.data.chapterList];
      if (chapters.value.length > 0) {
        activeChapter.value = chapters.value[0].id;
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

    if (response.data.ret === 0 && response.data.exercisesList) {
      const allExercises = Array.isArray(response.data.exercisesList) ? response.data.exercisesList : [response.data.exercisesList];
      exercises.value = allExercises.filter(ex => ex.is_official === 1 || ex.is_official === '1');
    } else {
      exercises.value = [];
      ElMessage.error('获取习题列表失败：' + response.data.msg);
    }
  } catch (error) {
    console.error('获取习题列表失败', error);
    ElMessage.error('网络请求失败，请稍后重试');
    exercises.value = [];
  } finally {
    loading.value = false;
  }
};

const selectChapter = (chapter: Chapter) => {
  activeChapter.value = chapter.id;
  selectedExercise.value = null; // 切换章节时清空选中的习题
};

const selectExercise = async (exercise: Exercise) => {
  selectedExercise.value = exercise;
  
  // 如果习题已提交，获取历史作答记录
  if (exercise.is_committed === 1) {
    await getExerciseHistory(exercise.exercise_id);
  }
};

const backToList = () => {
  selectedExercise.value = null;
  currentAnswer.value = '';
};

const submitAnswer = async () => {
  if (!selectedExercise.value || !currentAnswer.value.trim()) {
    ElMessage.warning('请填写答案后再提交');
    return;
  }
  
  submitting.value = true;
  try {
    const formData = new FormData();
    formData.append('exercise_id', selectedExercise.value.exercise_id.toString());
    formData.append('student_answer', currentAnswer.value);
    
    const response = await axios.post(`${store.ip}/api/student/commitExercise`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 5000
    });
    
    if (response.data.ret === 0) {
      // 提交成功，更新本地数据
      selectedExercise.value.student_answer = currentAnswer.value;
      selectedExercise.value.submitted_at = new Date().toISOString();
      selectedExercise.value.is_committed = 1;
      
      // 更新exercises列表中的对应项
      const exerciseIndex = exercises.value.findIndex(ex => ex.exercise_id === selectedExercise.value!.exercise_id);
      if (exerciseIndex !== -1) {
        exercises.value[exerciseIndex] = { ...selectedExercise.value };
      }
      
      // 清空当前答案输入
      currentAnswer.value = '';
      
      ElMessage.success('答案提交成功！');
    } else {
      ElMessage.error(response.data.msg || '提交失败，请重试');
    }
  } catch (error) {
    console.error('提交答案失败:', error);
    ElMessage.error('提交失败，请重试');
  } finally {
    submitting.value = false;
  }
};

const editAnswer = () => {
  // 已作答的题目不允许重新作答
  if (selectedExercise.value?.is_committed === 1) {
    ElMessage.warning('该题目已提交，不可重新作答');
    return;
  }
  
  if (selectedExercise.value?.student_answer) {
    currentAnswer.value = selectedExercise.value.student_answer;
  }
};

/**
 * 获取习题历史作答记录
 */
const getExerciseHistory = async (exerciseId: number) => {
  try {
    const formData = new FormData();
    formData.append('exercise_id', exerciseId.toString());
    
    const response = await axios.post(`${store.ip}/api/student/getExerciseHistory`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 5000
    });
    
    if (response.data.ret === 0) {
      // 习题已作答且批改
      if (selectedExercise.value) {
        selectedExercise.value.student_answer = response.data.student_answer;
        selectedExercise.value.submitted_at = response.data.answer_time;
      }
    } else if (response.data.ret === 2) {
      // 习题未作答
      if (selectedExercise.value) {
        selectedExercise.value.is_committed = 0;
      }
    } else if (response.data.ret === 3) {
      // 习题已作答但未批改
      if (selectedExercise.value) {
        selectedExercise.value.student_answer = response.data.student_answer;
        selectedExercise.value.submitted_at = response.data.answer_time;
      }
    }
  } catch (error) {
    console.error('获取习题历史记录失败:', error);
  }
};

/**
 * 将英文习题类型转换为中文显示
 * @param {string} type - 习题类型
 * @returns {string} 中文类型名称
 */
const getExerciseTypeText = (type: string): string => {
  const typeMap: Record<string, string> = {
    'choices': '选择题',
    'blanks': '填空题',
    'answers': '问答题',
    'coding': '编程题',
    'true_false': '判断题'
  };
  return typeMap[type] || type;
};

/**
 * Markdown 渲染器实例
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
 * 将 Markdown 内容转换为纯文本并截取指定长度
 * @param {string} content - Markdown 格式的内容
 * @param {number} maxLength - 最大显示字符数
 * @returns {string} 处理后的纯文本
 */
const formatExerciseContent = (content: string, maxLength: number = 50): string => {
  if (!content) return '';
  
  // 将 Markdown 转换为 HTML
  const html = marked.parse(content);
  
  // 创建临时 DOM 元素来解析 HTML
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;
  
  // 获取纯文本内容
  const plainText = tempDiv.textContent || tempDiv.innerText || '';
  
  // 截取指定长度并添加省略号
  return plainText.length > maxLength ? plainText.substring(0, maxLength) + '...' : plainText;
};

</script>

<style scoped>
.course-page {
  display: flex;
  height: 100%;
  background-color: #f5f7fa;
}

.left-panel {
  width: 300px;
  min-width: 300px;
  flex-shrink: 0;
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
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.exercise-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.exercise-content {
  font-size: 16px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
  flex: 1;
  width: 100%;
  max-width: 100%;
  color: #303133;
  font-weight: 500;
}

.exercise-meta {
  font-size: 12px;
  color: #606266;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.exercise-type {
  background-color: #f0f2f5;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.exercise-difficulty {
  color: #909399;
}

.exercise-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  background-color: #f56c6c;
  color: white;
}

.exercise-status.submitted {
  background-color: #67c23a;
  color: white;
}

.exercise-detail {
  padding: 24px;
}

.question-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-header h2 {
  margin: 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.question-meta {
  display: flex;
  gap: 8px;
}

.question-content {
  background: white;
  padding: 20px;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  line-height: 1.6;
  color: #303133;
  text-align: left;
}

.answer-section {
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.answer-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
}

.submit-time {
  color: #909399;
  font-size: 14px;
}

.submitted-answer {
  text-align: left;
}

.submitted-answer .answer-content {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  margin-bottom: 15px;
}

.submitted-answer pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  color: #303133;
  line-height: 1.5;
}

.answer-input, .re-answer {
  margin-top: 10px;
}

.answer-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.re-answer {
  margin-top: 20px;
  padding-top: 20px;
}

.back-button {
  margin-bottom: 20px;
}

.exercise-detail h3 {
  line-height: 1.6;
  color: #303133;
  margin-bottom: 20px;
}

.exercise-detail h1,
.exercise-detail h2,
.exercise-detail h3,
.exercise-detail h4,
.exercise-detail h5,
.exercise-detail h6 {
  margin-top: 16px;
  margin-bottom: 12px;
  font-weight: 600;
}

.exercise-detail p {
  line-height: 1.6;
  margin-bottom: 12px;
}

.exercise-detail ul,
.exercise-detail ol {
  margin-bottom: 12px;
  padding-left: 20px;
}

.exercise-detail li {
  margin-bottom: 4px;
}

.exercise-detail code {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.exercise-detail pre {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 12px;
}

.exercise-detail pre code {
  background: none;
  padding: 0;
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

/* 题目内容 Markdown 样式 - Typora风格 */
.question-content {
  line-height: 1.7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  color: #2c3e50;
}

/* 标题样式 */
.question-content h1,
.question-content h2,
.question-content h3,
.question-content h4,
.question-content h5,
.question-content h6 {
  margin: 24px 0 16px 0;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
}

.question-content h1 {
  font-size: 2em;
  border-bottom: 2px solid #eaecef;
  padding-bottom: 12px;
  margin-bottom: 20px;
}

.question-content h2 {
  font-size: 1.6em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.question-content h3 {
  font-size: 1.3em;
}

.question-content h4 {
  font-size: 1.1em;
}

.question-content h5 {
  font-size: 1em;
}

.question-content h6 {
  font-size: 0.9em;
  color: #6a737d;
}

/* 段落样式 */
.question-content p {
  margin: 16px 0;
  text-align: justify;
  text-justify: inter-ideograph;
}

/* 列表样式 */
.question-content ul,
.question-content ol {
  margin: 16px 0;
  padding-left: 24px;
}

.question-content li {
  margin: 8px 0;
  line-height: 1.6;
}

.question-content ul li {
  list-style-type: disc;
}

.question-content ol li {
  list-style-type: decimal;
}

/* 嵌套列表 */
.question-content ul ul,
.question-content ol ol,
.question-content ul ol,
.question-content ol ul {
  margin: 4px 0;
}

/* 行内代码样式 */
.question-content code {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 3px;
  padding: 2px 6px;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', monospace;
  font-size: 0.85em;
  color: #d73a49;
}

/* 代码块样式 */
.question-content pre {
  background-color: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  font-size: 0.85em;
  line-height: 1.45;
}

.question-content pre code {
  background: none;
  border: none;
  padding: 0;
  color: #24292e;
  font-size: inherit;
}

/* 引用样式 */
.question-content blockquote {
  border-left: 4px solid #dfe2e5;
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  background-color: #f8f9fa;
  border-radius: 0 3px 3px 0;
}

.question-content blockquote p {
  margin: 12px 0;
}

/* 表格样式 */
.question-content table {
  border-collapse: collapse;
  margin: 20px 0;
  width: 100%;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  overflow: hidden;
}

.question-content th,
.question-content td {
  border: 1px solid #d0d7de;
  padding: 12px 16px;
  text-align: left;
  vertical-align: top;
}

.question-content th {
  background-color: #f6f8fa;
  font-weight: 600;
  color: #24292e;
}

.question-content tr:nth-child(even) {
  background-color: #f6f8fa;
}

.question-content tr:hover {
  background-color: #f1f8ff;
}

/* 链接样式 */
.question-content a {
  color: #0969da;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

.question-content a:hover {
  color: #0550ae;
  border-bottom-color: #0969da;
}

.question-content a:visited {
  color: #8250df;
}

/* 强调样式 */
.question-content strong {
  font-weight: 600;
  color: #24292e;
}

.question-content em {
  font-style: italic;
  color: #656d76;
}

/* 分隔线样式 */
.question-content hr {
  border: none;
  height: 2px;
  background-color: #d0d7de;
  margin: 24px 0;
  border-radius: 1px;
}

/* 删除线样式 */
.question-content del {
  text-decoration: line-through;
  color: #656d76;
}

/* 高亮样式 */
.question-content mark {
  background-color: #fff8c5;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 图片样式 */
.question-content img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 任务列表样式 */
.question-content input[type="checkbox"] {
  margin-right: 8px;
  transform: scale(1.1);
}

.question-content .task-list-item {
  list-style: none;
  margin-left: -20px;
}

/* 键盘按键样式 */
.question-content kbd {
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
.question-content p:first-child {
  margin-top: 0;
}

.question-content p:last-child {
  margin-bottom: 0;
}

.question-content code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #e6a23c;
}

.question-content pre {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  overflow-x: auto;
  margin: 16px 0;
}

.question-content pre code {
  background: none;
  padding: 0;
  color: #303133;
}

.question-content strong {
  font-weight: 600;
  color: #303133;
}

.question-content blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  background: #f8f9fa;
  border-left: 4px solid #409eff;
  color: #606266;
}

</style>