<template>
  <div class="my-courses">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">我的课程</h1>
    </div>

    <!-- 搜索栏 -->
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        placeholder="搜索课程名称或讲师"
        clearable
        class="search-input"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 课程列表 -->
    <div class="courses-container">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>
      
      <div v-else-if="filteredCourses.length === 0" class="empty-state">
        <el-empty description="暂无课程数据">
        </el-empty>
      </div>
      
      <div v-else class="courses-list">
        <div 
          v-for="course in filteredCourses" 
          :key="course.id"
          class="course-item"
          @click="openCourse(course)"
        >
          
          <div class="course-info">
            <h3 class="course-title">{{ course.name }}</h3>
            <p class="course-instructor">讲师：{{ course.teacher_name }}</p>
            
            <div class="course-meta">
              <span class="course-students">
                <el-icon><User /></el-icon>
                {{ course.student_num }}人学习
              </span>
            </div>
          </div>
          

        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { User, Search } from '@element-plus/icons-vue';
import axios from 'axios';
import { mainStore } from '../../../store/index.ts';
import Course from '../Course/index.vue';

/**
 * 我的课程数据接口定义（基于API）
 */
interface MyCourse {
  id: number;
  name: string;
  teacher_id: number;
  teacher_name: string;
  student_num: number;
}

// 响应式数据
const searchQuery = ref('');
const myCourses = ref<MyCourse[]>([]);
const loading = ref(false);



/**
 * 获取学生已选课程列表
 */
const fetchMyCourses = async () => {
  loading.value = true;
  try {
    // 获取JWT token
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.warning('请先登录');
      return;
    }

    // 调用API获取学生课程列表，设置5秒超时
    const response = await axios.get(`${store.ip}/api/student/getCourseList`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      timeout: 5000
    });

    if (response.data.ret === 0) {
      // 处理API返回的课程数据，确保courseList是数组格式
      const courseList = response.data.courseList;
      if (courseList) {
        myCourses.value = Array.isArray(courseList) ? courseList : [courseList];
      } else {
        myCourses.value = [];
      }
    } else {
      myCourses.value = [];
      ElMessage.error('获取课程列表失败：' + response.data.msg);
    }
  } catch (error) {
    console.error('获取我的课程失败:', error);
    ElMessage.error('网络请求失败，请稍后重试');
    myCourses.value = [];
  } finally {
    loading.value = false;
  }
};

/**
 * 根据搜索关键词过滤课程
 */
const filteredCourses = computed(() => {
  if (!searchQuery.value.trim()) {
    return myCourses.value;
  }
  return myCourses.value.filter(course => 
    course.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    course.teacher_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});



const store = mainStore();

/**
 * 打开课程页面
 * @param course 课程对象
 */
const openCourse = (course: MyCourse) => {
  store.addTab(`${course.name}`, Course, { courseData: course });
};



/**
 * 组件挂载时的初始化操作
 */
onMounted(() => {
  fetchMyCourses();
});
</script>

<style scoped>
.my-courses {
  padding: 24px;
  background-color: transparent;
  min-height: 100%;
  font-family: Arial, Helvetica, sans-serif;
}

/* 页面标题样式 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0 0 8px 0;
}

/* 搜索栏样式 */
.search-container {
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
}

.search-input {
  max-width: 400px;
  width: 100%;
  height: 40px;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

/* 筛选器样式 */
.course-filters {
  background: white;
  border-radius: 8px;
  padding: 0 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px var(--shadowColor);
}

.course-filters :deep(.el-tabs__header) {
  margin: 0;
}

.course-filters :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

/* 课程容器样式 */
.courses-container {
  background: transparent;
  overflow: hidden;
  margin-left: 2rem;
  margin-right: 2rem;
}

.loading-state {
  padding: 24px;
}

.empty-state {
  padding: 60px 20px;
}

/* 课程列表样式 */
.courses-list {
  padding: 0;
}

.course-item {
  display: flex;
  align-items: center;
  padding: 24px;
  margin-bottom: 1rem;
  background-color: #f8f8f8f8;
  transition: background-color 0.2s ease;
  cursor: pointer;
  border-radius: 8px;
}

.course-item:last-child {
  border-bottom: none;
}

.course-item:hover {
  background-color: #fafbfc;
}


/* 课程信息样式 */
.course-info {
  flex: 1;
  min-width: 0;
}

.course-title {
  font-size: 18px;
  font-weight: 600;
  color: #213244;
  line-height: 1.4;
  margin-bottom: 3px;
}

.course-instructor {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 8px 0;
}

.course-description {
  font-size: 14px;
  color: #5a6c7d;
  margin: 0 0 12px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.course-students {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #7f8c8d;
}



/* 响应式设计 */
@media (max-width: 768px) {
  .my-courses {
    padding: 16px;
  }
  
  .course-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 20px;
    
  }
  
  .course-image {
    width: 100%;
    height: 160px;
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .course-actions {
    width: 100%;
    justify-content: space-between;
    margin-left: 0;
    margin-top: 16px;
  }
  
  .course-meta {
    gap: 12px;
  }
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

@media (max-width: 480px) {
  .page-title {
    font-size: 24px;
  }
  
  .course-filters {
    padding: 0 16px;
  }
  
  .course-item {
    padding: 16px;
  }
  
  .course-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .course-actions .el-button {
    width: 100%;
  }
}
</style>