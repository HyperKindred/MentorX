<template>
  <div class="main">
    <div class="left-panel">
      <div class="left-title">往日习题</div>
      <div class="practice-list">
        <div v-if="isGenerating" class="practice-item generating">
          <span class="practice-date">{{ todayDate }} (生成中...)</span>
        </div>
        <div 
          v-for="practice in practices" 
          :key="practice.exercise_id" 
          class="practice-item" 
          :class="{active: activePractice === practice.exercise_id}" 
          @click="selectPractice(practice)"
        >
          <span class="practice-date">{{ formatDate(practice.date) }}</span>
          <div class="status-indicator" :class="getStatusClass(practice.check)"></div>
        </div>
      </div>
      <div class="practice-calendar">
        <!-- 日历组件 -->
        <div class="calendar-container">
          <div class="calendar-header">
            <button class="nav-btn" @click="prevMonth">
              <i class="fas fa-chevron-left"></i>
            </button>
            <h3>{{ currentYear }}年{{ currentMonth + 1 }}月</h3>
            <button class="nav-btn" @click="nextMonth">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
          <div class="calendar-weekdays">
            <div v-for="day in ['日', '一', '二', '三', '四', '五', '六']" :key="day" class="weekday">
              {{ day }}
            </div>
          </div>
          <div class="calendar-days">
            <div 
              v-for="(day, index) in calendarDays" 
              :key="index" 
              class="day"
              :class="{
                'current-month': day.isCurrentMonth,
                'has-practice': day.hasPractice,
                'correct': day.check === 0,
                'wrong': day.check === 1,
                'c-w': day.check === 2
              }"
              @click="selectDay(day)"
            >
              {{ day.date }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-panel">
      <div class="right-title">每日一题</div>
      <div v-if="activePractice === -1" class="generating-message">
        <i class="fas fa-spinner fa-spin"></i>
        <p>每日习题正在生成中，请稍候...</p>
        <p>这可能需要几分钟时间</p>
      </div>
      <div v-else>
      <div class="content-area">
        <div class="practice-content" v-html="marked.parse( activePractice.exercise_content || '')"></div>
          <div class="answer-section">           
            <!-- 已批改状态：显示历史答案和批改结果 -->
            <div v-if="activePractice.is_committed" class="submitted-answer">
              <div class="answer-content">
                <h4>学生答案：</h4>
                <pre>{{ activePractice.student_answer }}</pre>
                <div v-if="activePractice.check" class="check-result">
                  <h4>批改结果：</h4>
                  <div class="check-score">
                    <div class="markdown-content" v-html="getCheckLabel(activePractice.check)"></div>
                  </div>
                  <div v-if="activePractice.analyse" class="check-analyse">
                    <h4>详细分析：</h4>
                    <div class="markdown-content" v-html="marked.parse(activePractice.analyse)"></div>
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
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { active } from 'sortablejs';
import { marked } from 'marked';
const store = mainStore();
const practices = ref([]);
const activePractice = ref('');
const currentDate = ref(new Date());
const currentYear = ref(currentDate.value.getFullYear());
const currentMonth = ref(currentDate.value.getMonth());
const currentAnswer = ref<string>('');
const checking = ref(false);
const todayDate = new Date().toISOString().split('T')[0];
const checkMap: Record<string, string> = {
  0:'✔️正确',
  1: '❌错误',
  2: '⭕半对半错'
};

const getCheckLabel = (type: string): string => {
  return checkMap[type] || '❓未批改';
};

const hasTodayPractice = computed(() => {
  return practices.value.some(p => p.date === todayDate);
});

const generatingPractice = computed(() => {
  return {
    exercise_id: -1, // 特殊ID，表示生成中
    date: todayDate,
    check: -1,
    isGenerating: true
  };
});

const sortedPractices = computed(() => {
  let list = [...practices.value];
  
  // 按日期倒序排序
  list.sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });
  
  // 添加生成中项（如果需要）
  if (isGenerating.value && !hasTodayPractice.value) {
    return [generatingPractice.value, ...list];
  }
  
  return list;
});

const getPracticeList = () => {
  axios.post(`${store.ip}/api/student/getDailyPracticeList`, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;
    if (data.ret === 0) {
      practices.value = Array.isArray(data.chapterList) 
        ? data.chapterList 
        : [data.chapterList];
      
      // 按日期倒序排序
      practices.value.sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      });
      
      // 如果生成了今日的练习，清除生成状态
      if (hasTodayPractice.value) {
        localStorage.removeItem('generatingStatus');
      }
      if (practices.value.length > 0) {
        selectPractice(practices.value[0]);
      }
    } else {
      practices.value = [];
      ElMessage.error('获取练习列表失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取练习列表失败：网络错误');
  });
};

const selectPractice = (practice: any) => {
  if (practice.isGenerating) {
    activePractice.value = -1;
  } else {
    activePractice.value = practice.exercise_id;
    const formData = new FormData();
    formData.append('exercise_id', activePractice.value.exercise_id);

    axios.post(`${store.ip}/api/student/getExerciseHistory`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      }
    }).then(res => {
      const data = res.data;
      if (data.ret === 0) {
        activePractice.student_answer = data.student_answer;
        activePractice.answer_time = data.answer_time;
        activePractice.check = data.check;
        activePractice.analyse = data.analyse;
      } else {
        ElMessage.error('获取作答情况失败：' + data.msg);
      }
    }).catch(() => {
      ElMessage.error('获取作答情况失败：网络错误');
    });
  }

};

const submitAndCheck = async () => {
  if (!activePractice.value || !currentAnswer.value.trim()) {
    ElMessage.warning('请填写答案后再提交');
    return;
  }
  
  checking.value = true;
  try {
    // 先提交答案
    const submitFormData = new FormData();
    submitFormData.append('exercise_id', activePractice.value.exercise_id.toString());
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
      checkFormData.append('Eno', activePractice.value.exercise_id.toString());
      
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
        activePractice.value.student_answer = currentAnswer.value;
        activePractice.value.submitted_at = new Date().toISOString();
        activePractice.value.is_committed = 1;
        
        // 更新practices列表中的对应项
        const practiceIndex = practices.value.findIndex(ex => ex.exercise_id === activePractice.value!.exercise_id);
        if (practiceIndex !== -1) {
          practices.value[practiceIndex] = { ...activePractice.value };
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

const calendarDays = computed(() => {
  const year = currentYear.value;
  const month = currentMonth.value;
  
  // 获取当月第一天是星期几（0-6，0为星期日）
  const firstDay = new Date(year, month, 1).getDay();
  // 获取当月天数
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  // 获取上个月天数
  const daysInPrevMonth = new Date(year, month, 0).getDate();
  
  const days = [];
  
  // 1. 添加上个月末尾的几天（填充日历开头）
  for (let i = firstDay - 1; i >= 0; i--) {
    const prevMonthDate = daysInPrevMonth - i;
    const date = new Date(year, month - 1, prevMonthDate);
    
    // 查找当天的练习状态
    const practice = practices.value.find(p => {
      const practiceDate = new Date(p.date);
      return (
        practiceDate.getFullYear() === date.getFullYear() &&
        practiceDate.getMonth() === date.getMonth() &&
        practiceDate.getDate() === date.getDate()
      );
    });
    
    days.push({
      date: prevMonthDate,
      isCurrentMonth: false,
      hasPractice: !!practice,
      check: practice?.check,
      practiceId: practice?.exercise_id
    });
  }
  
  // 2. 添加当月天数
  for (let i = 1; i <= daysInMonth; i++) {
    const date = new Date(year, month, i);
    
    // 查找当天的练习状态
    const practice = practices.value.find(p => {
      const practiceDate = new Date(p.date);
      return (
        practiceDate.getFullYear() === date.getFullYear() &&
        practiceDate.getMonth() === date.getMonth() &&
        practiceDate.getDate() === date.getDate()
      );
    });
    
    days.push({
      date: i,
      isCurrentMonth: true,
      hasPractice: !!practice,
      check: practice?.check,
      practiceId: practice?.exercise_id
    });
  }
  
  // 3. 添加下个月开始的几天（填充日历末尾）
  const totalCells = 42; // 6行 * 7列
  const nextMonthDays = totalCells - days.length;
  for (let i = 1; i <= nextMonthDays; i++) {
    days.push({
      date: i,
      isCurrentMonth: false,
      hasPractice: false
    });
  }
  
  return days;
});

// 切换月份
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
};

// 选择日期
const selectDay = (day: any) => {
  if (!day.isCurrentMonth || !day.hasPractice) return;
  
  // 查找对应的练习项
  const practice = practices.value.find(p => p.exercise_id === day.practiceId);
  if (practice) {
    selectPractice(practice);
  }
};

// 初始化
onMounted(() => {
  getPracticeList();
  if (isGenerating.value) {
    const pollInterval = setInterval(() => {
      getPracticeList();
      
      // 如果生成了今日练习或超过5分钟，停止轮询
      if (hasTodayPractice.value) {
        clearInterval(pollInterval);
      }
    }, 10000); // 每10秒检查一次
  }
});

// 格式化日期显示
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};

// 根据状态获取类名
const getStatusClass = (status: number) => {
  switch(status) {
    case 0: return 'correct';
    case 1: return 'wrong';
    case 2: return 'c-w';
    default: return '';
  }
};
</script>
<style scoped>
.main {
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

.left-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
  padding: 20px 20px 28px 20px;
}

.practice-list {
  padding-bottom: 20px;
  padding-left: 5px;
  padding-right: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  max-height: 40%; /* 为日历留出空间 */
}

.practice-item {
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

.practice-item:hover {
  background-color: var(--backgroundColor2);
  color: var(--titleColor);
}

.practice-item.active {
  background-color: transparent;
  color: var(--titleColor);
  background-color: var(--backgroundColor2);
  font-weight: 540;
}

.practice-date{
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

.practice-calendar {
  display: flex;
  flex-direction: column;
  padding: 10px;
  height: 60%; /* 占据左侧面板剩余空间 */
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.right-title {
  color: var(--titleColor);
  padding: 1rem;
  text-align: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 800;
}

/* 新增日历样式 */
.calendar-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 10px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.calendar-header h3 {
  margin: 0;
  font-size: 14px;
  color: var(--titleColor);
}

.nav-btn {
  background: transparent;
  border: none;
  border-radius: 5px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--textColor2);
  transition: all 0.2s;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--titleColor);
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-size: 12px;
  color: var(--textColor2);
  margin-bottom: 5px;
}

.weekday {
  padding: 3px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  flex: 1;
}

.day {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  font-size: 12px;
  height: 100%;
  color: var(--textColor2);
}

.day.current-month {
  color: var(--titleColor);
}

.day.has-practice {
  background: rgba(80, 80, 80, 0.1);
}

.day.correct {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.day.wrong {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.day.c-w {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.day:hover {
  background: rgba(255, 255, 255, 0.1);
}

.content-area {
  flex: 1;
  overflow-y: hidden;
  padding: 24px;
}

.practice-content {
  font-size: 16px;
  margin-bottom: 8px;
  overflow-y: auto;
  text-overflow: ellipsis;
  line-height: 1.4;
  flex: 1;
  width: 100%;
  max-width: 100%;
  color: #303133;
  font-weight: 500;
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

.answer-content h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: var(--textColor2);
  font-weight: 600;
}

.answer-content pre {
  background: var(--backgroundColor3);
  border: 1px solid var(--borderColor);
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
  border-top: 1px solid var(--borderColor);
}

.check-score {
  display: block;
  width: 100%;
  padding: 6px 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  background: var(--backgroundColor3);
  border: 1px solid var(--borderColor);
  box-sizing: border-box;
}


.check-analyse {
  background: var(--backgroundColor3);
  border: 1px solid var(--borderColor);
  border-radius: 4px;
  padding: 12px;
  margin-top: 12px;
}

.answer-input {
  margin-top: 8px;
}

.answer-actions {
  margin-top: 16px;
  text-align: right;
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

.practice-item.generating {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border-left: 3px solid #ffc107;
}

.generating-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #ffc107;
  padding: 20px;
}

.generating-message i {
  font-size: 48px;
  margin-bottom: 20px;
}

.generating-message p {
  margin: 5px 0;
  font-size: 16px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-left: 8px;
}

.status-indicator.correct {
  background-color: #28a745;
}

.status-indicator.wrong {
  background-color: #dc3545;
}

.status-indicator.c-w {
  background-color: #ffc107;
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