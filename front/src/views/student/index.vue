<template>
  <div class="student-dashboard">
    <!-- 导航标签页 -->
    <div class="dashboard-tabs">
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="推荐课程" name="recommended">
          <RecommendedCourses />
        </el-tab-pane>
        <el-tab-pane label="我的课程" name="my-courses">
          <MyCourses />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import RecommendedCourses from './RecommendedCourses/index.vue';
import MyCourses from './MyCourses/index.vue';

const store = mainStore();
const router = useRouter();
const message = ref('');
const activeTab = ref('recommended');

/**
 * 导航到指定组件
 * @param componentName 组件名称
 */
function navigateTo(componentName: string) {
  router.push({ name: componentName });
}

/**
 * 处理标签页切换事件
 * @param tab 标签页对象
 */
const handleTabClick = (tab: any) => {
  console.log('切换到标签页:', tab.props.name);
};

/**
 * 组件挂载时的初始化操作
 */
onMounted(() => {
  console.log('学生仪表板已加载');
});
</script>

<style scoped>
.student-dashboard {
  width: 100%;
  height: 100vh;
  background-color: #f5f7fa;
  overflow: hidden;
}

.dashboard-tabs {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.dashboard-tabs :deep(.el-tabs) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.dashboard-tabs :deep(.el-tabs__header) {
  margin: 0;
  background: white;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  z-index: 10;
}

.dashboard-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow: auto;
  padding: 0;
}

.dashboard-tabs :deep(.el-tab-pane) {
  height: 100%;
}

.dashboard-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.dashboard-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
}

.dashboard-tabs :deep(.el-tabs__item.is-active) {
  color: #409eff;
}
</style>