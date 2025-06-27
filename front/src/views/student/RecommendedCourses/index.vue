<template>
  <div class="recommended-courses">
    <!-- 搜索栏 -->
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

    <!-- 推荐课程标题 -->
    <div class="section-header">
      <h2 class="section-title">推荐课程</h2>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 课程卡片网格 -->
    <div v-else-if="filteredCourses.length > 0" class="courses-grid">
      <div 
        v-for="course in filteredCourses" 
        :key="course.id"
        class="course-card"
        @click="viewCourse(course)"
      >
        <div class="course-content">
          <h3 class="course-title">{{ course.name }}</h3>
          <p class="course-teacher">讲师：{{ course.teacher_name }}</p>
          <div class="course-meta">
            <span class="course-students">
              <el-icon><User /></el-icon>
              {{ course.student_num }}人学习
            </span>
            <el-button 
              v-if="!isCourseEnrolled(course.id)"
              class="join" 
              size="small" 
              :loading="joinLoading[course.id]"
              @click.stop="joinCourse(course)"
            >
              加入课程
            </el-button>
            <el-button 
              v-else
              class="joined" 
              size="small" 
              disabled
            >
              已加入
            </el-button>
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
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Search, User } from '@element-plus/icons-vue';
import axios from 'axios';
import { mainStore } from '../../../store/index.ts';

/**
 * 推荐课程数据接口定义（基于API）
 */
interface RecommendedCourse {
  id: number;
  name: string;
  teacher_id: number;
  teacher_name: string;
  student_num: number;
}

// 响应式数据
const searchQuery = ref('');
const courses = ref<RecommendedCourse[]>([]);
const enrolledCourses = ref<RecommendedCourse[]>([]);
const loading = ref(false);
const joinLoading = ref<Record<number, boolean>>({});
const store = mainStore();



/**
 * 根据搜索关键词过滤课程
 */
const filteredCourses = computed(() => {
  if (!searchQuery.value.trim()) {
    return courses.value;
  }
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    course.teacher_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

/**
 * 获取已选课程列表
 */
const fetchEnrolledCourses = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      return;
    }

    const response = await axios.get(`${store.ip}/api/student/getCourseList`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      timeout: 5000
    });

    if (response.data.ret === 0) {
      const courseList = response.data.courseList;
      if (courseList) {
        enrolledCourses.value = Array.isArray(courseList) ? courseList : [courseList];
      } else {
        enrolledCourses.value = [];
      }
    }
  } catch (error) {
    console.error('获取已选课程列表失败:', error);
  }
};

/**
 * 获取课程列表
 */
const fetchCourses = async () => {
  try {
    loading.value = true;
    
    // 设置请求超时时间为5秒
    const response = await axios.get(`${store.ip}/api/getCourseList`, {
      timeout: 5000
    });
    
    if (response.data.ret === 0) {
      // 服务器返回的是CourseList数组，确保courseList是数组格式
      const courseList = response.data.courseList;
      if (courseList) {
        courses.value = Array.isArray(courseList) ? courseList : [courseList];
      } else {
        courses.value = [];
      }
    } else {
      ElMessage.error(response.data.msg || '获取课程列表失败');
      courses.value = [];
    }
  } catch (error) {
    console.error('获取课程列表失败:', error);
    courses.value = [];
    ElMessage.error('网络请求失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

/**
 * 加入课程
 */
const joinCourse = async (course: RecommendedCourse) => {
  try {
    // 设置当前课程的加载状态
    joinLoading.value[course.id] = true;
    
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.warning('请先登录');
      return;
    }

    // 创建FormData对象，使用multipart/form-data格式发送课程ID
    const formData = new FormData();
    formData.append('course_id', course.id.toString());

    // 设置请求超时时间为3秒
    const response = await axios.post(`${store.ip}/api/student/joinCourse`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      },
      timeout: 3000
    });

    console.log(response)

    if (response.data.ret === 0) {
      ElMessage.success('成功加入课程');
      // 更新学生人数
      course.student_num += 1;
      // 将课程添加到已选课程列表中
      enrolledCourses.value.push({
        id: course.id,
        name: course.name,
        teacher_id: course.teacher_id,
        teacher_name: course.teacher_name,
        student_num: course.student_num
      });
    } else {
      ElMessage.error(response.data.msg || '加入课程失败');
    }
  } catch (error) {
    console.error('加入课程失败:', error);
    ElMessage.error('网络请求失败，请稍后重试');
  } finally {
    // 清除加载状态
    joinLoading.value[course.id] = false;
  }
};

/**
 * 查看课程详情
 */
const viewCourse = (course: RecommendedCourse) => {
  // 这里可以添加路由跳转到课程详情页
};

/**
 * 检查课程是否已选
 */
const isCourseEnrolled = (courseId: number): boolean => {
  return enrolledCourses.value.some(course => course.id === courseId || course.course_id === courseId);
};

/**
 * 组件挂载时的初始化操作
 */
onMounted(async () => {
  await fetchEnrolledCourses();
  await fetchCourses();
  console.log('推荐课程组件已加载');
});
</script>

<style scoped>
.recommended-courses {
  font-family: Arial, Helvetica, sans-serif;
  padding: 20px;
  background-color: transparent;
  min-height: 100%;
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

/* 搜索栏样式 */
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: none;
  letter-spacing: 0.1rem;
}

/* 章节标题样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  margin-left: 1rem;
}

.section-title {
  font-size: 30px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
}

.join {
    padding: 0.4rem 1rem;
    background-color: #417dff;
    color: white;
    border: 1px solid #fff;
    outline: none;
    cursor: pointer;
    width: 5rem;
    border-radius: 8px;
    transition: all 100ms ease-in;
    margin: 0.6rem 0;
    font-size: 0.6rem;
    padding: 0.5rem 0;
}

.join:hover {
  background-color: #417dffd8;
}

.joined {
    padding: 0.4rem 1rem;
    background-color: #233f7b91;
    color: white;
    border: 1px solid #fff;
    outline: none;
    cursor: pointer;
    width: 5rem;
    border-radius: 8px;
    transition: all 100ms ease-in;
    margin: 0.6rem 0;
    font-size: 0.6rem;
    padding: 0.5rem 0;
}

.joined:hover {
    background-color: #233f7b91;
    color: white;
}

/* 课程网格布局 */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 0;
  margin-left: 1rem;
  margin-right: 1rem;
}

/* 课程卡片样式 */
.course-card {
  background: #fdfffff0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px var(--shadowColor);
  transition: all 0.3s ease;
  color: #080808;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px var(--shadowColor2);
}



.course-content {
  color: #080808;
  padding: 20px;
  padding-bottom: 5px;
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
</style>