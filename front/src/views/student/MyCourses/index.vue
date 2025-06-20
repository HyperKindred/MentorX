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
          
          <div class="course-actions">
            <el-button type="primary" @click="viewDetails(course)">
              查看详情
            </el-button>
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

/**
 * 我的课程数据接口定义（基于API）
 */
interface MyCourse {
  id: number;
  name: string;
  teacher_id: number;
  teacher_name: string;
  student_num: number;
  image?: string;
}

// 响应式数据
const activeTab = ref('all');
const searchQuery = ref('');
const myCourses = ref<MyCourse[]>([]);
const loading = ref(false);

// 模拟数据作为后备
const mockCourses: MyCourse[] = [
  {
    id: 1,
    name: 'Vue.js 3.0 完整开发教程',
    teacher_id: 1,
    teacher_name: '张老师',
    student_num: 1250,
    image: '/src/assets/images/vue-course.jpg'
  },
  {
    id: 2,
    name: 'Python数据分析实战',
    teacher_id: 2,
    teacher_name: '李教授',
    student_num: 890,
    image: '/src/assets/images/python-course.jpg'
  },
  {
    id: 3,
    name: '机器学习基础',
    teacher_id: 3,
    teacher_name: '王博士',
    student_num: 2100,
    image: '/src/assets/images/ml-course.jpg'
  }
];

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
      myCourses.value = mockCourses;
      return;
    }

    // 调用API获取学生课程列表
    const response = await axios.get('/api/student/getCourseList', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.data.ret === 0) {
      // 处理API返回的课程数据
      myCourses.value = response.data.courseList.map((course: any) => ({
        id: course.course_id,
        name: course.course_name,
        teacher_id: course.teacher_id,
        teacher_name: course.teacher_name,
        student_num: course.student_num || 0,
      }));
      ElMessage.success('课程列表加载成功');
    } else {
      throw new Error(response.data.msg || '获取课程列表失败');
    }
  } catch (error) {
    console.error('获取我的课程失败:', error);
    ElMessage.warning('获取课程列表失败，使用模拟数据');
    // 使用模拟数据作为后备
    myCourses.value = mockCourses;
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



/**
 * 查看课程详情
 * @param course 课程对象
 */
const viewDetails = (course: MyCourse) => {
  ElMessage.info(`查看课程详情：${course.name}`);
};



/**
 * 组件挂载时的初始化操作
 */
onMounted(() => {
  console.log('我的课程组件已加载');
  fetchMyCourses();
});
</script>

<style scoped>
.my-courses {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题样式 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

/* 搜索栏样式 */
.search-container {
  margin-bottom: 24px;
  display: flex;
  justify-content: flex-start;
}

.search-input {
  max-width: 400px;
  width: 100%;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.course-filters :deep(.el-tabs__header) {
  margin: 0;
}

.course-filters :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

/* 课程容器样式 */
.courses-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  border-bottom: 1px solid #f0f2f5;
  transition: background-color 0.2s ease;
}

.course-item:last-child {
  border-bottom: none;
}

.course-item:hover {
  background-color: #fafbfc;
}

/* 课程图片样式 */
.course-image {
  position: relative;
  width: 120px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 20px;
  flex-shrink: 0;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}



/* 课程信息样式 */
.course-info {
  flex: 1;
  min-width: 0;
}

.course-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
  line-height: 1.4;
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



/* 课程操作样式 */
.course-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 20px;
}

.course-menu {
  margin-left: 8px;
}

.menu-btn {
  padding: 8px;
  color: #7f8c8d;
}

.menu-btn:hover {
  color: #409eff;
  background-color: #f0f9ff;
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