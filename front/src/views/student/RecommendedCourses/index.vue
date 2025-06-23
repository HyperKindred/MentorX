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
              type="primary" 
              size="small" 
              :loading="joinLoading[course.id]"
              @click.stop="joinCourse(course)"
            >
              加入课程
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
const loading = ref(false);
const joinLoading = ref<Record<number, boolean>>({});
const store = mainStore();

/**
 * 模拟课程数据
 */
const mockCourses: RecommendedCourse[] = [
  {
    id: 1,
    name: 'Vue.js 3.0 完整开发教程',
    teacher_id: 1,
    teacher_name: '张老师',
    student_num: 1250
  },
  {
    id: 2,
    name: 'Python数据分析实战',
    teacher_id: 2,
    teacher_name: '李教授',
    student_num: 890
  },
  {
    id: 3,
    name: '机器学习基础',
    teacher_id: 3,
    teacher_name: '王博士',
    student_num: 2100
  },
  {
    id: 4,
    name: 'React 现代开发实践',
    teacher_id: 4,
    teacher_name: '陈老师',
    student_num: 1680
  },
  {
    id: 5,
    name: 'Node.js 后端开发',
    teacher_id: 5,
    teacher_name: '刘教授',
    student_num: 950
  },
  {
    id: 6,
    name: 'TypeScript 进阶指南',
    teacher_id: 6,
    teacher_name: '赵老师',
    student_num: 720
  }
];

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
      // 根据API响应结构处理数据
      const courseList = response.data.courseList;
      if (courseList && courseList.course) {
        // 如果返回的是单个课程对象，转换为数组
        courses.value = Array.isArray(courseList.course) ? courseList.course : [courseList.course];
      } else {
        courses.value = [];
      }
    } else {
      ElMessage.error(response.data.msg || '获取课程列表失败');
      // 使用模拟数据作为备用
      courses.value = mockCourses;
      ElMessage.info('已切换到模拟数据模式');
    }
  } catch (error) {
    console.error('获取课程列表失败:', error);
    // 请求失败或超时时使用模拟数据
    courses.value = mockCourses;
    ElMessage.warning('网络请求失败，已切换到模拟数据模式');
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

    // 设置请求超时时间为3秒
    const response = await axios.post('/api/student/joinCourse', {
      course_id: course.id
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      timeout: 3000
    });

    if (response.data.ret === 0) {
      ElMessage.success('成功加入课程');
      // 更新学生人数
      course.student_num += 1;
    } else {
      ElMessage.error(response.data.msg || '加入课程失败');
      // 模拟加入成功（备用逻辑）
      course.student_num += 1;
      ElMessage.info('模拟加入课程成功');
    }
  } catch (error) {
    console.error('加入课程失败:', error);
    // 请求失败或超时时的模拟处理
    course.student_num += 1;
    ElMessage.warning('网络请求失败，已模拟加入课程');
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
 * 组件挂载时的初始化操作
 */
onMounted(() => {
  fetchCourses();
  console.log('推荐课程组件已加载');
});
</script>

<style scoped>
.recommended-courses {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 搜索栏样式 */
.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
  padding: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
}

.search-input {
  max-width: 600px;
  width: 100%;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: none;
}

/* 章节标题样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.more-btn {
  color: #409eff;
  font-size: 14px;
  padding: 0;
}

.more-btn:hover {
  color: #66b1ff;
}

/* 课程网格布局 */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 0;
}

/* 课程卡片样式 */
.course-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.course-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.course-card:hover .course-image img {
  transform: scale(1.05);
}

.course-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(64, 158, 255, 0.9);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.course-content {
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
</style>