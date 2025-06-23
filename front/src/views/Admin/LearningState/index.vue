<template>
  <div class="Main">
    <div class="student-list">
      <div class="student-item" v-for="item in students" :key="item.id">
        <div class="name">姓名：{{ item.name }} </div>
        <div class="student-item-course" v-for="item1 in item.courses" :key="item1.id">
            <div class="course_name">{{ item1.name }} </div>
            <div class="student-item-chapter" v-for="item2 in item1.chapters" :key="item2.id">
                <div class="chapter_name">章节：{{ item2.name }} </div>
                <div class="AIFrequence">AI使用次数：{{ item2.AIFrequence }} </div>
                <div class="correctness">答题准确率：{{ item2.correctness }} </div>
            </div>
        </div>
      </div>
    </div>
     <div class="course-list">
      <div class="course-item" v-for="item in courses" :key="item.id">
        <div class="course_name">{{ item.name }} </div>
        <div class="course-item-chapter" v-for="item1 in item.chapters" :key="item1.id">
            <div class="chapter_name">章节：{{ item1.name }} </div>
            <div class="AIFrequence">AI使用次数：{{ item1.AIFrequence }} </div>
            <div class="correctness">答题准确率：{{ item1.correctness }} </div>
        </div>
      </div>
    </div>   
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const students = ref([]);
const courses = ref([]);


onMounted(() => {
    getStudentsList();
    getCoursesList();
});

const getStudentsList = () => {
  const formData = new FormData();
  axios.post(`${store.ip}/api/getLearningStatsByPerson`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0 && Array.isArray(data.students)) {
      students.value = data.students;
    } else {
      students.value = []; 
      ElMessage.error('获取学习情况(按学生)失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学习情况(按学生)失败：网络错误');
  });
};

const getCoursesList = () => {
  const formData = new FormData();
  axios.post(`${store.ip}/api/getLearningStatsByCourse`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0 && Array.isArray(data.courses)) {
      courses.value = data.courses;
    } else {
      courses.value = []; 
      ElMessage.error('获取学习情况(按课程)失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取学习情况(按课程)失败：网络错误');
  });
};

</script>

<style scoped>

.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.exercise-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid #ddd;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.question-text {
  flex: 1;
  max-width: 70%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-weight: 500;
  color: #333;
}

.difficulty {
  flex-shrink: 0;
  color: #666;
  font-size: 14px;
  margin-left: 12px;
}

.type {
  flex-shrink: 0;
  color: grey;
  font-size: 14px;
  margin-left: 12px;
}

</style>