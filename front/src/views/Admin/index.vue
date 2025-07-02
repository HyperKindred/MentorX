<template>
  <div class="main">
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索课程"
        class="search-input"
        size="large"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
    <div class="section-header">
      <h2 class="section-title">课程列表</h2>
    </div>
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 课程卡片网格 -->
    <div v-else-if="filteredCourses.length > 0" class="courses-grid">
      <div 
        v-for="course in filteredCourses" 
        :key="course.id"
        class="course-card"
        @click="handleCardClick(course.id, course.name)"
      >
        <div class="course-content">
          <h3 class="course-title">{{ course.name }}</h3>
          <p class="course-teacher">讲师：{{ course.teacher_name }}</p>
          <div class="course-meta">
            <span class="course-students">
              <el-icon><User /></el-icon>
              {{ course.student_num }}人学习
            </span>
            <el-button type="primary" @click.stop="deleteCourse(course.id)">删除</el-button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <el-empty description="暂无课程数据"></el-empty>
    </div>
  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { mainStore } from '../../store/index.ts';
import { User, Search } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import A_chapter from './Chapter/index.vue'
const store = mainStore();
const courses = ref<Course[]>([]);
const loading = ref(false);
const searchQuery = ref('');

onMounted(() => {
  getCourseList();
});

interface Course {
  id: number;
  name: string;
  teacher_id: number;
  teacher_name: string;
  student_num: number;
}

const filteredCourses = computed(() => {
  if (!searchQuery.value.trim()) {
    return courses.value;
  }
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    course.teacher_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const getCourseList = () => {
  loading.value = true;
  axios({
    method: 'get',
    url: `${store.ip}/api/getCourseList`,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 0) {
        if (Array.isArray(responseData.courseList)){
          courses.value = Array.isArray(responseData.courseList) ? responseData.courseList : [responseData.courseList];
        }
        else {
          courses.value = [];
        }
      } else {
        ElMessage({
          message: '获取课程列表失败：' + responseData.msg,
          type: 'error',
        });
      }
    })
    .catch((error) => {
      courses.value = [];
      console.error('Error posting data:', error);
      ElMessage({
        message: '获取课程列表失败：网络错误，请稍后重试！',
        type: 'error',
        duration: 5000,
        grouping: true,
      });
    });
    loading.value = false;
};

const deleteCourse = (id: number) => {
  const formData = new FormData();
  formData.append('id', id)
  axios({
    method: 'post',
    url: `${store.ip}/api/deleteCourse`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('删除课程成功！');
        getCourseList();
      } else {
        ElMessage.error('删除课程失败：' + res.msg);
      }
    })
    .catch(() => {
      ElMessage.error('请求失败，请稍后重试！');
    });
}

const handleCardClick = (id: number, name: string) => {
  localStorage.setItem('selectedCourseId', id);
  localStorage.setItem('selectedCourseName', name);
  store.addTab(name, A_chapter);
};


</script>

<style scoped>
.main {
  font-family: Arial, Helvetica, sans-serif;
  padding: 20px;
  background-color: transparent;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.h2 {
    margin: 0.2rem;
    font-size: 1rem;
}

.p {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 100;
    margin: 1.2rem 0;
    letter-spacing: 0.1rem;
}


.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  padding: 20px 0;
  
}

.search-input {
  max-width: 600px;
  width: 100%;
  letter-spacing: 0.1rem;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 4px 12px var(--shadowColor);
  border: none;
  letter-spacing: 0.1rem;
}


.section-header {
  display: flex;
  align-items: center;
  justify-content: left;
  margin-bottom: 24px;
  margin-left: 1rem;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 0;
  margin-left: 1rem;
  margin-right: 1rem;
}


.course-card {
  background: rgba(255, 255, 255, 0.835);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px var(--shadowColor);
  transition: all 0.3s ease;
  color: #080808;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px var(--shadowColor2);
}


.add-input {
  border: none;
}


.course-content {
  color: #080808;
  padding: 20px;
}

.course-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-teacher {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 12px 0;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.course-students {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #666;
  flex: 1;
}

.course-students .el-icon {
  font-size: 16px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px; /* or any other height */
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
  .courses-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .course-card {
    padding: 16px;
  }
}
</style>
