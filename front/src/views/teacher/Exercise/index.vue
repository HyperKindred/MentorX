<template>
  <div class="Main">
    <!-- 题目内容 -->
    <div class="exercise-section">
      <div class="question">{{ exercise.content }}</div>
      <div class="meta">
        <span>题型：{{ getTypeLabel(exercise.type) }}</span>
        <span>难度等级：{{ exercise.difficulty }}</span>
      </div>
      <div class="answer">标准答案：{{ exercise.answer }}</div>
    </div>

    <!-- 学生作答列表 -->
    <div class="student-section">
      <div
        class="student-item"
        v-for="student in paginatedStudents"
        :key="student.student_id"
        @click="showAnalysis(student)"
      >
        <div class="student-name">学生姓名：{{ student.student_name }}</div>
        <div class="student-answer">作答内容：{{ student.student_answer }}</div>
        <div class="answer-time">作答时间：{{ student.answer_time }}</div>
        <div class="correction">
            <span v-if="student.check is null">❓</span>
            <span v-else-if="student.check === 1">✔️</span>
            <span v-else-if="student.check === 0">❌</span>
            <span v-else-if="student.check === 2">⭕</span>
        </div>

        <el-button type="primary" size="small" @click="ansChecker(student)" :disabled="student.is_checked === 1">
            批改习题
        </el-button>
      </div>
    </div>

    <!-- 分页器 -->
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
<el-dialog v-model="analysisDialogVisible" title="批改结果分析" width="500px">
  <p><strong>学生：</strong>{{ selectedStudent?.student_name }}</p>
  <p><strong>作答内容：</strong>{{ selectedStudent?.student_answer }}</p>
  <p>
    <strong>批改结果：</strong>
    <span v-if="selectedStudent?.check === 0">❌ 错误</span>
    <span v-else-if="selectedStudent?.check === 1">✔️ 正确</span>
    <span v-else-if="selectedStudent?.check === 2">⭕ 半对半错</span>
    <span v-else>❓ 未批改</span>
  </p>
  <p v-if="selectedStudent?.check != null && selectedStudent?.analyse">
    <strong>分析：</strong>{{ selectedStudent?.analyse }}
  </p>
  <template #footer>
    <span class="dialog-footer">
      <el-button @click="analysisDialogVisible = false">关闭</el-button>
    </span>
  </template>
</el-dialog>


</template>

<script lang="ts" setup>
import { ref, onMounted, computed    } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const router = useRouter();
const exercise = ref<Record<string, any>>({});
const students = ref<any[]>([]);
const selectedStudent = ref<any>(null);
const currentPage = ref(1);
const pageSize = 4;
const analysisDialogVisible = ref(false);
const selectedStudent = ref<any>(null);


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
      Authorization: localStorage.getItem('token'),
    }
  }).then(res => {
    if (res.data.ret === 0 && res.data.students?.student) {
      students.value = Array.isArray(res.data.students.student)
        ? res.data.students.student
        : [res.data.students.student];
    } else {
      ElMessage.error('获取学生作答情况失败：' + res.data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学生作答情况失败：网络错误');
  });
}

const ansChecker = (student: any) => {
  if (student.is_checked === 1) {
    ElMessage.warning('该学生的习题已批改');
    return;
  }

  const formData = new FormData();
  formData.append('Eno', exercise.value.id);
  formData.append('ans', student.student_answer);

  axios
    .post(`${store.ip}/api/teacher/checkExercise`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: localStorage.getItem('token'),
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


onMounted(() => {
    exercise.value = JSON.parse(localStorage.getItem('selectedExercise') || '{}');
    if (exercise.value?.id) {
    getExercisesAns();
    }
});



</script>

<style scoped>
.Main {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: rgba(135, 206, 250, 0.1);
  padding: 20px;
  box-sizing: border-box;
}

.exercise-section {
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 24px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.question {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.meta {
  color: #666;
  font-size: 14px;
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
}

.answer {
  font-size: 15px;
  color: #2c3e50;
  margin-top: 4px;
}

.student-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.student-item {
  background: #fff;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.student-name,
.student-answer,
.answer-time {
  margin-bottom: 6px;
  font-size: 14px;
  color: #444;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.correction {
  margin: 8px 0;
  font-weight: bold;
  color: #333;
}

</style>