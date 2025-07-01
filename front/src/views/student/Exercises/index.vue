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
             type="default" 
             :icon="Document" 
             class="function-btn"
             @click="openCourseware"
           >
             课件学习
           </el-button>
           <el-button 
             type="primary" 
             :icon="Edit" 
             class="function-btn active"
             disabled
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
                <span class="exercise-difficulty">难度: {{ getExerciseDifficultyText(exercise.difficulty) }}</span>
                <span class="exercise-type">{{ getExerciseTypeText(exercise.type) }}</span>
                <span class="exercise-status" :class="{ 'submitted': exercise.is_committed === 1, 'graded': exercise.is_committed === 1 && (exercise.check !== undefined || exercise.analyse) }">
                  {{ exercise.is_committed === 1 ? (exercise.check !== undefined || exercise.analyse ? '已批改' : '已提交') : '未提交' }}
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
                <span class="exercise-difficulty-1">难度: {{ getExerciseDifficultyText(selectedExercise.difficulty) }}</span>
                <el-tag type="info">{{ getExerciseTypeText(selectedExercise.type) }}</el-tag>
                <el-tag v-if="selectedExercise.is_committed && (selectedExercise.check !== undefined || selectedExercise.analyse)" type="success">已批改</el-tag>
                <el-tag v-else-if="selectedExercise.is_committed" type="warning">已提交</el-tag>
                <el-tag v-else type="danger">未提交</el-tag>
              </div>
            </div>
            <div class="question-content markdown-content" v-html="marked.parse(selectedExercise.exercise_content)"></div>
          </div>
          
          <!-- 作答区域 -->
          <div class="answer-section">
            <div class="answer-header">
              <h3>{{ selectedExercise.is_committed ? '历史答题内容' : '作答区' }}</h3>
              <div v-if="selectedExercise.is_committed && selectedExercise.submitted_at" class="submit-time">
                提交时间: {{ new Date(selectedExercise.submitted_at).toLocaleString() }}
              </div>
            </div>
            
            <!-- 已提交状态：显示历史答案和批改结果 -->
            <div v-if="selectedExercise.is_committed" class="submitted-answer">
              <div class="answer-content">
                <h4>学生答案：</h4>
                <pre>{{ selectedExercise.student_answer }}</pre>
                <div v-if="selectedExercise.check !== undefined || selectedExercise.analyse" class="check-result">
                  <h4>批改结果：</h4>
                  <div v-if="selectedExercise.check !== undefined" class="check-score" :class="getScoreClass(selectedExercise.check)">
                    <div class="markdown-content" v-html="marked.parse(selectedExercise.check)"></div>
                  </div>
                  <div v-if="selectedExercise.analyse" class="check-analyse">
                    <h4>详细分析：</h4>
                    <div class="markdown-content" v-html="marked.parse(selectedExercise.analyse)"></div>
                  </div>
                </div>
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
import { ref, onMounted, watch, onActivated } from 'vue';
import { ElMessage } from 'element-plus';
import { Document, Edit, Notebook, ChatDotRound } from '@element-plus/icons-vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { marked } from 'marked';
import Course from '../Course/index.vue';
import Practice from '../Practice/index.vue';
import AiAssistant from '../AiAssistant/index.vue';

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
  check?: string;
  analyse?: string;
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
const exercises = ref<Exercise[]>([]);
const loading = ref(false);
const selectedExercise = ref<Exercise | null>(null);
const currentAnswer = ref<string>('');
const submitting = ref(false);



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
      const filteredExercises = allExercises.filter(ex => ex.is_official === 1 || ex.is_official === '1');
      
      // 为每个已提交的习题获取批改状态
      const exercisesWithStatus = await Promise.all(
        filteredExercises.map(async (exercise) => {
          if (exercise.is_committed === 1) {
            try {
              const historyFormData = new FormData();
              historyFormData.append('exercise_id', exercise.exercise_id.toString());
              
              const historyResponse = await axios.post(`${store.ip}/api/student/getExerciseHistory`, historyFormData, {
                headers: {
                  'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                timeout: 5000
              });
              
              if (historyResponse.data.ret === 0) {
                // 习题已作答且批改
                exercise.student_answer = historyResponse.data.student_answer;
                exercise.submitted_at = historyResponse.data.answer_time;
                exercise.check = historyResponse.data.check;
                exercise.analyse = historyResponse.data.analyse;
              } else if (historyResponse.data.ret === 3) {
                // 习题已作答但未批改
                exercise.student_answer = historyResponse.data.student_answer;
                exercise.submitted_at = historyResponse.data.answer_time;
                exercise.check = undefined;
                exercise.analyse = undefined;
              }
            } catch (error) {
              console.error(`获取习题${exercise.exercise_id}历史记录失败:`, error);
            }
          }
          return exercise;
        })
      );
      
      exercises.value = exercisesWithStatus;
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
        selectedExercise.value.check = response.data.check;
        selectedExercise.value.analyse = response.data.analyse;
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
        // 未批改状态，清空批改结果
        selectedExercise.value.check = undefined;
        selectedExercise.value.analyse = undefined;
      }
    }
  } catch (error) {
    console.error('获取习题历史记录失败:', error);
  }
};

/**
 * 获取习题类型的中文显示文本
 * @param {string} type - 习题类型
 * @returns {string} 中文显示文本
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
 * 获取习题难度的中文显示文本
 * @param {number} difficulty - 难度等级数字
 * @returns {string} 中文显示文本
 */
const getExerciseDifficultyText = (difficulty: number): string => {
  const difficultyMap: Record<number, string> = {
    1: '容易',
    2: '中等',
    3: '困难',
    4: '极难'
  };
  return difficultyMap[difficulty] || `难度${difficulty}`;
};

/**
 * 根据分数获取样式类名
 * @param {number} score - 分数
 * @returns {string} 样式类名
 */
const getScoreClass = (score: number): string => {
  if (score >= 90) return 'excellent';
  if (score >= 80) return 'good';
  if (score >= 60) return 'pass';
  return 'fail';
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
 * 导航到课件学习页面
 */
const openCourseware = () => {
  if (courseInfo.value && chapters.value.length > 0) {
    store.addTab('课件学习', Course, {
      courseData: courseInfo.value,
      chapterData: chapters.value,
      activeChapterId: activeChapter.value
    });
  } else {
    ElMessage.warning('课程信息不完整，无法跳转');
  }
};

/**
 * 导航到个人练习页面
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
 * 导航到AI助手页面
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
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}

.left-panel {
  width: 300px;
  background: var(--backgroundColor2);
  border-right: 1.5px solid transparent;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
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
  border: 1px solid #f8f8f8;
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
  justify-content: end;
  align-items: center;
  flex-shrink: 0;
}

.exercise-difficulty {
  color: #909399;
  margin-right: 1rem;
}

.exercise-difficulty-1 {
  color: #909399;
  margin-right: 0.8rem;
  font-size: 0.9rem;
}

.exercise-type {
  background-color: #417dff;
  color: white;
  padding: 2px 8px;
  margin-right: 1rem;
  border-radius: 4px;
  font-weight: 500;
}



.exercise-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  background-color: #f56c6c;
  color: white;
}

.exercise-status.submitted {
  background-color: #74dc3f;
  color: white;
}

.exercise-status.graded {
  background-color: #409eff;
  color: white;
}

.exercise-detail {
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.question-section {
  margin-bottom: 30px;
  padding: 20px;
  background: var(--backgroundColor3);
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
  color: var(--textColor);
  font-size: 20px;
  font-weight: 600;
}

.question-meta {
  display: flex;
  gap: 8px;
}

.question-content {
  background: var(--backgroundColor3);
  padding: 20px;
  border-radius: 6px;
  border: 1px solid var(--borderColor);
  line-height: 1.6;
  text-align: left;
}

.answer-section {
  padding: 20px;
  background: var(--backgroundColor3);
  border-radius: 8px;
  border: 1px solid var(--borderColor);
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--borderColor);
}

.answer-header h3 {
  margin: 0;
  color: var(--textColor);
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
  background: var(--backgroundColor3);
  padding: 15px;
  border-radius: 6px;
  border: 1px solid var(--borderColor);
  margin-bottom: 15px;
}

.submitted-answer pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  color: var(--textColor);
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

.answer-actions .el-button {
  min-width: 120px;
}

/* 批改结果样式 */
.answer-content h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: var(--textColor2);
  font-weight: 600;
}

.answer-content pre {
  background: var(--backgroundColor3);
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 12px;
  margin: 0 0 16px 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
}

.check-result {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e4e7ed;
}

.check-score {
  display: block;
  width: 100%;
  padding: 6px 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  background: white;
  border: 1px solid #e4e7ed;
  box-sizing: border-box;
}

/* .check-score.excellent {
  background-color: #f0f9ff;
  color: #1890ff;
  border: 1px solid #b3d8ff;
}

.check-score.good {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.check-score.pass {
  background-color: #fff7e6;
  color: #fa8c16;
  border: 1px solid #ffd591;
}

.check-score.fail {
  background-color: #fff2f0;
  color: #ff4d4f;
  border: 1px solid #ffb3b3;
} */

.check-analyse {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 12px;
  margin-top: 12px;
}

.re-answer {
  margin-top: 20px;
  padding-top: 20px;
}

.back-button {
  margin-bottom: 20px;
  align-self: flex-end;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
  padding: 20px 20px 28px 20px;
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
  width: 270px;
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



.chapter-title {
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

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
  border: 1.5px solid var(--textColor2);
  background-color: var(--backgroundColor);
  color: var(--textColor2);
}

.function-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadowColor2);
  color: var(--textColor);
  border: 1.5px solid var(--textColor2);
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
/* 骨架屏自定义样式 - 适配深蓝色背景 */
.loading-state :deep(.el-skeleton__item) {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.loading-state :deep(.el-skeleton__p) {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 768px) {
  .left-panel {
    width: 240px;
  }
  
  .chapter-list {
    padding: 0 8px 20px 8px;
  }
  
  .content-area {
    padding: 16px;
  }
  
  .function-buttons {
    padding: 16px 20px;
  }
}



</style>