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
      
      <!-- 生成习题区域 -->
      <div class="generate-section">
        <h3 class="nav-title">生成习题</h3>
        <div class="generate-form">
          <div class="form-item">
            <label>题目类型：</label>
            <el-select v-model="generateForm.type" placeholder="选择题目类型">
              <el-option label="选择题" value="choices"></el-option>
              <el-option label="填空题" value="blanks"></el-option>
              <el-option label="问答题" value="answers"></el-option>
              <el-option label="编程题" value="code"></el-option>
            </el-select>
          </div>
          <div class="form-item">
            <label>难度等级：</label>
            <el-select v-model="generateForm.difficulty" placeholder="选择难度">
              <el-option label="容易" :value="1"></el-option>
              <el-option label="中等" :value="2"></el-option>
              <el-option label="困难" :value="3"></el-option>
              <el-option label="极难" :value="4"></el-option>
            </el-select>
          </div>
          <el-button 
            @click="generateExercise" 
            type="primary" 
            :loading="generating"
            :disabled="!activeChapter || !generateForm.type || !generateForm.difficulty"
            class="generate-btn"
          >
            {{ generating ? '生成中...' : '生成习题' }}
          </el-button>
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
             type="default" 
             :icon="Edit" 
             class="function-btn"
             @click="openExercises"
           >
             章节习题
           </el-button>
           <el-button 
             type="primary" 
             :icon="Notebook" 
             class="function-btn active"
             disabled
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
        <div v-else-if="practices.length === 0" class="empty-state">
          <el-empty description="暂无个人练习"></el-empty>
        </div>
        <div v-else-if="!selectedPractice">
          <div class="practice-list">
            <div v-for="practice in practices" :key="practice.exercise_id" class="practice-item" @click="selectPractice(practice)">
              <div class="practice-content">{{ formatPracticeContent(practice.exercise_content, 80) }}</div>
              <div class="practice-meta">
                <span class="practice-difficulty">难度: {{ getPracticeDifficultyText(practice.difficulty) }}</span>
                <span class="practice-type">{{ getPracticeTypeText(practice.type) }}</span>
                <span class="practice-status" :class="{ 'submitted': practice.is_committed === 1 }">
                  {{ practice.is_committed === 1 ? '已批改' : '未批改' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="practice-detail">
          <el-button @click="backToList" class="back-button">返回列表</el-button>
          
          <!-- 题目区域 -->
          <div class="question-section">
            <div class="question-header">
              <h2>题目内容</h2>
              <div class="question-meta">
                <span class="practice-difficulty-1">难度: {{ getPracticeDifficultyText(selectedPractice.difficulty) }}</span>
                <el-tag type="info">{{ getPracticeTypeText(selectedPractice.type) }}</el-tag>
                <el-tag v-if="selectedPractice.is_committed" type="success">已批改</el-tag>
                <el-tag v-else type="danger">未批改</el-tag>
              </div>
            </div>
            <div class="question-content" v-html="marked.parse(selectedPractice.exercise_content)"></div>
          </div>
          
          <!-- 作答区域 -->
          <div class="answer-section">
            <div class="answer-header">
              <h3>{{ selectedPractice.is_committed ? '历史答题内容' : '作答区' }}</h3>
              <div v-if="selectedPractice.is_committed && selectedPractice.submitted_at" class="submit-time">
                提交时间: {{ new Date(selectedPractice.submitted_at).toLocaleString() }}
              </div>
            </div>
            
            <!-- 已批改状态：显示历史答案和批改结果 -->
            <div v-if="selectedPractice.is_committed" class="submitted-answer">
              <div class="answer-content">
                <h4>学生答案：</h4>
                <pre>{{ selectedPractice.student_answer }}</pre>
                <div v-if="selectedPractice.check_result" class="check-result">
                  <h4>批改结果：</h4>
                  <div class="check-score" :class="getScoreClass(selectedPractice.check_result)">
                    评分: {{ selectedPractice.check_result }}
                  </div>
                  <div v-if="selectedPractice.analyse" class="check-analyse">
                    <h4>详细分析：</h4>
                    <div v-html="marked.parse(selectedPractice.analyse)"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 未批改状态：显示作答区和批改按钮 -->
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
                <el-button @click="submitAndCheck" type="primary" :loading="checking">
                  {{ checking ? '批改中...' : '提交并批改' }}
                </el-button>
              </div>
            </div>
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
import Exercises from '../Exercises/index.vue';
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

interface Practice {
  exercise_id: number;
  type: string;
  difficulty: number;
  exercise_content: string;
  is_official: string | number;
  is_committed?: number;
  student_answer?: string;
  submitted_at?: string;
  check_result?: string;
  analyse?: string;
}

interface GenerateForm {
  type: string;
  difficulty: number | null;
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
const practices = ref<Practice[]>([]);
const loading = ref(false);
const selectedPractice = ref<Practice | null>(null);
const currentAnswer = ref<string>('');
const checking = ref(false);
const generating = ref(false);
const generateForm = ref<GenerateForm>({
  type: '',
  difficulty: null
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
    getPracticeList(newChapterId);
  }
});

const getChapterList = async (courseId: number) => {
  try {
    const formData = new FormData();
    formData.append('id', courseId.toString());
    const response = await axios.post(`${store.ip}/api/getChapterList`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
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

const getPracticeList = async (chapterId: number) => {
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
      const allPractices = Array.isArray(response.data.exercisesList) ? response.data.exercisesList : [response.data.exercisesList];
      practices.value = allPractices.filter(ex => ex.is_official !== 1 && ex.is_official !== '1');
    } else {
      practices.value = [];
      ElMessage.error('获取练习列表失败：' + response.data.msg);
    }
  } catch (error) {
    console.error('获取练习列表失败', error);
    ElMessage.error('网络请求失败，请稍后重试');
    practices.value = [];
  } finally {
    loading.value = false;
  }
};

const selectChapter = (chapter: Chapter) => {
  activeChapter.value = chapter.id;
  selectedPractice.value = null; // 切换章节时清空选中的练习
};

const selectPractice = async (practice: Practice) => {
  selectedPractice.value = practice;
  
  // 如果习题已批改，获取历史作答记录
  if (practice.is_committed === 1) {
    await getPracticeHistory(practice.exercise_id);
  }
};

const backToList = () => {
  selectedPractice.value = null;
  currentAnswer.value = '';
};

/**
 * 生成习题
 */
const generateExercise = async () => {
  if (!activeChapter.value || !generateForm.value.type || !generateForm.value.difficulty) {
    ElMessage.warning('请选择章节、题目类型和难度等级');
    return;
  }
  
  generating.value = true;
  try {
    const formData = new FormData();
    formData.append('ChapterNo', activeChapter.value.toString());
    formData.append('difficulty', generateForm.value.difficulty.toString());
    formData.append('type', generateForm.value.type);
    
    const response = await axios.post(`${store.ip}/api/student/generate_exercises`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 120000 // 生成习题可能需要较长时间
    });
    
    if (response.data.ret === 0) {
      ElMessage.success('习题生成成功！');
      // 重新获取练习列表
      await getPracticeList(activeChapter.value);
      // 重置生成表单
      generateForm.value = {
        type: '',
        difficulty: null
      };
    } else {
      ElMessage.error(response.data.msg || '生成习题失败，请重试');
    }
  } catch (error) {
    console.error('生成习题失败:', error);
    ElMessage.error('生成习题失败，请重试');
  } finally {
    generating.value = false;
  }
};

/**
 * 提交答案并批改
 */
const submitAndCheck = async () => {
  if (!selectedPractice.value || !currentAnswer.value.trim()) {
    ElMessage.warning('请填写答案后再提交');
    return;
  }
  
  checking.value = true;
  try {
    // 先提交答案
    const submitFormData = new FormData();
    submitFormData.append('exercise_id', selectedPractice.value.exercise_id.toString());
    submitFormData.append('student_answer', currentAnswer.value);
    
    const submitResponse = await axios.post(`${store.ip}/api/student/commitExercise`, submitFormData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 5000
    }); 
    
    if (submitResponse.data.ret === 0) {
      // 提交成功后进行批改
      const checkFormData = new FormData();
      checkFormData.append('Eno', selectedPractice.value.exercise_id.toString());
      
      const checkResponse = await axios.post(`${store.ip}/api/student/check_exercises`, checkFormData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        timeout: 120000 // 批改可能需要较长时间
      });
      
      if (checkResponse.data.ret === 0) {
        // 批改成功，获取批改结果
        await getPracticeHistory(selectedPractice.value.exercise_id);
        
        // 更新本地数据
        selectedPractice.value.student_answer = currentAnswer.value;
        selectedPractice.value.submitted_at = new Date().toISOString();
        selectedPractice.value.is_committed = 1;
        
        // 更新practices列表中的对应项
        const practiceIndex = practices.value.findIndex(ex => ex.exercise_id === selectedPractice.value!.exercise_id);
        if (practiceIndex !== -1) {
          practices.value[practiceIndex] = { ...selectedPractice.value };
        }
        
        // 清空当前答案输入
        currentAnswer.value = '';
        
        ElMessage.success('答案提交并批改成功！');
      } else {
        ElMessage.error(checkResponse.data.msg || '批改失败，请重试');
      }
    } else {
      ElMessage.error(submitResponse.data.msg || '提交失败，请重试');
    }
  } catch (error) {
    console.error('提交并批改失败:', error);
    ElMessage.error('提交并批改失败，请重试');
  } finally {
    checking.value = false;
  }
};

/**
 * 获取练习历史作答记录
 */
const getPracticeHistory = async (exerciseId: number) => {
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
      if (selectedPractice.value) {
        selectedPractice.value.student_answer = response.data.student_answer;
        selectedPractice.value.submitted_at = response.data.answer_time;
        selectedPractice.value.check_result = response.data.check;
        selectedPractice.value.analyse = response.data.analyse;
      }
    } else if (response.data.ret === 2) {
      // 习题未作答
      if (selectedPractice.value) {
        selectedPractice.value.is_committed = 0;
      }
    } else if (response.data.ret === 3) {
      // 习题已作答但未批改
      if (selectedPractice.value) {
        selectedPractice.value.student_answer = response.data.student_answer;
        selectedPractice.value.submitted_at = response.data.answer_time;
      }
    }
  } catch (error) {
    console.error('获取练习历史记录失败:', error);
  }
};

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
 * 导航到章节习题页面
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
 * 将英文练习类型转换为中文显示
 */
const getPracticeTypeText = (type: string): string => {
  const typeMap: Record<string, string> = {
    'choices': '选择题',
    'blanks': '填空题',
    'answers': '问答题',
    'code': '编程题',
    'coding': '编程题',
    'true_false': '判断题'
  };
  return typeMap[type] || type;
};

/**
 * 获取练习难度的中文显示文本
 * @param {number} difficulty - 难度等级数字
 * @returns {string} 中文显示文本
 */
const getPracticeDifficultyText = (difficulty: number): string => {
  const difficultyMap: Record<number, string> = {
    1: '容易',
    2: '中等',
    3: '困难',
    4: '极难'
  };
  return difficultyMap[difficulty] || `难度${difficulty}`;
};

/**
 * 根据评分获取样式类名
 */
const getScoreClass = (score: string): string => {
  const numScore = parseInt(score);
  if (numScore >= 90) return 'excellent';
  if (numScore >= 80) return 'good';
  if (numScore >= 60) return 'pass';
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
 * 将 Markdown 内容转换为纯文本并截取指定长度
 */
const formatPracticeContent = (content: string, maxLength: number = 50): string => {
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
  background: transparent;
  border-right: 1.5px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.course-header {
  padding: 24px 20px;
  border-bottom: 1.5px solid #e4e7ed;
  background: transparent;
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

.practice-item {
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

.practice-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.practice-content {
  font-size: 16px;
  margin-bottom: 12px;
  color: #303133;
}

.practice-meta {
  font-size: 14px;
  color: #606266;
}

.practice-detail {
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.back-button {
  margin-bottom: 20px;
  align-self: flex-end;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
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
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid #f8f8f8;
  color: #aaaaaa;
}

.chapter-item:hover {
  background-color: transparent;
    color: #f8f8f8;
  border-color: #e4e7ed;
}

.chapter-item.active {
  background-color: transparent;
  border-color: #f8f8f8;
  color: #f8f8f8;
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

.chapter-title {
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

.chapter-item.active .chapter-number {
  background-color: #409eff;
  color: white;
}



.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* 功能按钮组样式 */
.function-buttons {
  border-bottom: 1.5px solid #e4e7ed;
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
  border: 1px solid #d9d9d9;
}

.function-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.function-btn.active {
  background: linear-gradient(135deg, #409eff 0%, #66b3ff 100%);
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

.practice-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.practice-item {
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

.practice-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.practice-content {
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

.practice-meta {
  font-size: 12px;
  color: #606266;
  display: flex;
  justify-content: end;
  align-items: center;
  flex-shrink: 0;
}

/* 生成习题区域样式 */
.generate-section {
  border-top: 1px solid #e4e7ed;
  padding: 20px;
}

.generate-form {
  padding: 0 8px;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  font-size: 14px;
  color: #f8f8f8;
  margin-bottom: 8px;
  font-weight: 500;
}

.generate-btn {
  width: 100%;
  margin-top: 8px;
}

/* 题目区域样式 */
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

/* Markdown 内容样式 - Typora风格 */
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
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #e6a23c;
}

/* 代码块样式 */
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

/* 引用样式 */
.question-content blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  background: #f8f9fa;
  border-left: 4px solid #409eff;
  color: #606266;
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
  color: #303133;
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



/* 作答区域样式 */
.answer-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e4e7ed;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f2f5;
}

.answer-header h3 {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
}

.submit-time {
  font-size: 14px;
  color: #909399;
}

.submitted-answer {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 16px;
  text-align: left;
}

.answer-content h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #606266;
  font-weight: 600;
}

.answer-content pre {
  background: white;
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
  display: inline-block;
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: 600;
  margin-bottom: 12px;
}

.check-score.excellent {
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
}

.check-analyse {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 16px;
  margin-top: 12px;
}

.answer-input {
  margin-top: 8px;
}

.answer-actions {
  margin-top: 16px;
  text-align: right;
}

.practice-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  background-color: #f56c6c;
  color: white;
}

.practice-status.submitted {
  background-color: #74dc3f;
  color: white;
}

.practice-type {
  background-color: #417dff;
  color: white;
  padding: 2px 8px;
  margin-right: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.practice-difficulty {
  color: #909399;
  margin-right: 1rem;
}

.practice-difficulty-1 {
  color: #909399;
  margin-right: 0.8rem;
  font-size: 0.9rem;
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

/* 响应式设计 */
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