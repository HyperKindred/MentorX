<template>
  <div class="main">
    <!-- 题目内容 -->
    <div class="exercise-section">
      <div class="exercise-title">
        <h2>题目内容</h2>
      </div>
      <div class="exercise-content" v-html="marked.parse(exercise.content || '')"></div>
      <div class="meta">
        <span class="exercise-difficulty">难度: {{ exercise.difficulty }}</span>
        <span class="exercise-type">{{ getTypeLabel(exercise.type) }}</span>
      </div>
      <div class="answer">
        <strong>标准答案：</strong>
        <div v-html="marked.parse(exercise.answer || '')"></div>
      </div>
    </div>

    <!-- 学生作答列表 -->
    <div class="student-section">
      <div class="student-title">
        <h2>学生作答</h2>
      </div>
      <div
        class="student-item"
        v-for="student in paginatedStudents"
        :key="student.student_id"
        @click="showAnalysis(student)"
      >
        <div class="student-name">{{ student.student_name }}</div>
        <div class="student-answer">作答内容：{{ student.student_answer }}</div>
        <div class="student-buttom">
          <div class="answer-time">{{ student.answer_time }}</div>
          <div class="buttom-right">
          <div class="correction">
              <span v-if="student.check === 0">✔️</span>
              <span v-else-if="student.check === 1">❌</span>
              <span v-else-if="student.check === 2">⭕</span>
              <span v-else>❓</span>
          </div>
          <el-button type="primary" size="small" @click="ansChecker(student)" :disabled="student.is_checked === 1" class="check_btn">
              批改习题
          </el-button>
          </div>
        </div>

      </div>
    <div class="pagination">
      <el-pagination
        layout="prev, pager, next"
        :page-size="pageSize"
        :current-page="currentPage"
        :total="students.length"
        @current-change="handlePageChange"
        background
      />
    </div>
    </div>

  </div>
<el-dialog v-model="analysisDialogVisible" title="批改结果分析" width="700px" class="analysis" style="padding: 2rem; text-align: left;">
  <p class="analysis-info"><strong>学生：</strong>{{ selectedStudent?.student_name }}</p>
  <p class="analysis-info"><strong>作答内容：</strong>{{ selectedStudent?.student_answer }}</p>
  <p class="analysis-info">
    <strong>批改结果：</strong>
    <span v-if="selectedStudent?.check === 1">❌错误</span>
    <span v-else-if="selectedStudent?.check === 0">✔️正确</span>
    <span v-else-if="selectedStudent?.check === 2">⭕半对半错</span> 
    <span v-else>❓未批改</span>
  </p>
  <p v-if="selectedStudent?.check != null && selectedStudent?.analyse">
    <strong>分析：</strong>
    <div class="analysis-content" v-html="marked.parse(selectedStudent.analyse)"></div>
  </p>

</el-dialog>


</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { marked } from 'marked';
const store = mainStore();
const router = useRouter();
const exercise = ref<Record<string, any>>({});
const students = ref<any[]>([]);
const selectedStudent = ref<any>(null);
const currentPage = ref(1);
const pageSize = 4;
const analysisDialogVisible = ref(false);


const typeMap: Record<string, string> = {
  choices: '选择题',
  blanks: '填空题',
  answers: '简答题'
};

const getTypeLabel = (type: string): string => {
  return typeMap[type] || '未知题型';
};

const getExercisesAns = () => {
  const formData = new FormData();
  formData.append('exercise_id', exercise.value.id);
  axios.post(`${store.ip}/api/teacher/getStudentExercises`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    if (res.data.ret === 0) {
      if (Array.isArray(res.data.students)){
      students.value = res.data.students;
        }
      else{
        students.value = [];
      }
    } else {
      ElMessage.error('获取学生作答情况失败：' + res.data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学生作答情况失败：网络错误');
  });
}

const ansChecker = (student: any) => {
  if (student.check) {
    ElMessage.warning('该学生的习题已批改');
    return;
  }

  const formData = new FormData();
  formData.append('Eno', exercise.value.id);
  formData.append('student_id', student.student_id);
  axios
    .post(`${store.ip}/api/teacher/check`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    .then((res) => {
      if (res.data.ret === 0) {
        getExercisesAns();
        selectedStudent.value = student;
        ElMessage.success('批改成功');
      } else {
        ElMessage.error('批改失败：' + res.data.msg);
      }
    })
    .catch(() => {
      ElMessage.error('批改失败：网络错误');
    });
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
};

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return students.value.slice(start, start + pageSize);
});

const showAnalysis = (student: any) => {
  selectedStudent.value = student;
  analysisDialogVisible.value = true;
};

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

onMounted(() => {
    exercise.value = JSON.parse(localStorage.getItem('selectedExercise') || '{}');
    if (exercise.value?.id) {
    getExercisesAns();
    }
});



</script>

<style scoped>
.main {
  display: flex;
  height: 100%;
  background-color: transparent;
}
.exercise-section {
  width: 900px;
  background: transparent;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  border-right: 1rem;
  padding-left: 1rem;
}


.exercise-content {
  padding-top: 1rem;
  font-size: 16px;
  line-height: 1.6;
  flex: 1;
  width: 100%;
  color: #303133;
  font-weight: 500;
  white-space: normal;
  overflow-y: auto;
  text-overflow: initial;
  text-align: left;
  padding-left: 3rem;
  padding-right: 3rem;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  background: #f8f8f8;
}

.meta {
  font-size: 12px;
  color: #606266;
  display: flex;
  justify-content: end;
  align-items: center;
  flex-shrink: 0;
  padding-top: 0.4rem;
  padding-left: 3rem;
  padding-right: 3rem;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  background: #f8f8f8;
  padding-bottom: 0.5rem;
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

.answer {
  font-size: 15px;
  color: #2c3e50;
  margin-top: 0.5rem;
  white-space: normal;
  text-align: left;
  padding-left: 3rem;
  padding-right: 3rem;
  border-radius: 5px;
  background: #f8f8f8;
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.student-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
  padding-left: 2rem;
  padding-right: 2rem
}

.student-item {
  background: #fff;
  padding-top: 16px;
  padding-left: 16px;
  padding-right: 16px;
  padding-bottom: 5px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  margin-bottom: 1rem;
  text-align: left;
}

.student-name {
  font-size: 16px;
  color: black;
  margin-bottom: 0.5rem;

}
.student-answer {
  font-size: 14px;
  color: #080808;
}
.answer-time {
  margin-bottom: 6px;
  font-size: 14px;
  color: #909399;
  left: 1rem;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.correction {
  font-weight: bold;
  color: #333;
  margin-right: 0.5rem;
}

.check_btn  {
  right: 1rem;
  left: auto;
}

.exercise-content p,
.answer p {
  margin: 0 0 8px 0;
}

.exercise-content ul,
.answer ul {
  margin: 8px 0 8px 1em;
  padding-left: 1.2em;
}

.exercise-content code,
.answer code {
  background-color: #f2f2f2;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}

.student-buttom {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}


.analysis-content {
  margin-left: 1rem;
}
.analysis-info {
  margin-bottom: 0.5rem;
}

.buttom-right {
  display: flex;
  flex-direction: row;
  justify-content: end;
}
</style>