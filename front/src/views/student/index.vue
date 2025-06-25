<template>
  <div class="student-dashboard">
    <RecommendedCourses />
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
 * 组件挂载时的初始化操作
 */
onMounted(() => {
});
</script>

<style scoped>
.student-dashboard {
  width: 100%;
  height: 100%;
  background-color: transparent;
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
  background: rgb(186, 186, 186);
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