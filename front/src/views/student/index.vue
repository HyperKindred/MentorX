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

// 获取今日日期字符串 (YYYY-MM-DD)
const getTodayDate = () => {
  const today = new Date();
  return today.toISOString().split('T')[0];
};

// 检查今日是否已生成习题
const hasGeneratedToday = () => {
  const today = getTodayDate();
  const generationDate = localStorage.getItem('lastGeneratedDate');
  
  // 检查本地存储中是否有今日的记录
  return generationDate === today;
};

// 设置生成状态
const setGeneratingStatus = (status: boolean) => {
  localStorage.setItem('generatingStatus', status.toString());
};

// 获取生成状态
const getGeneratingStatus = (): boolean => {
  return localStorage.getItem('generatingStatus') === 'true';
};

// 记录生成日期
const recordGenerationDate = () => {
  localStorage.setItem('lastGeneratedDate', getTodayDate());
};

// 生成每日习题
const generateDailyPractice = () => {
  // 检查今日是否已生成过
  if (hasGeneratedToday()) {
    console.log('今日已生成过习题，跳过生成');
    return;
  }
  
  // 设置生成状态
  setGeneratingStatus(true);
  
  axios.post(`${store.ip}/api/student/generateDailyPractice`, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;
    if (data.ret === 0) {
      ElMessage.success('每日习题已生成！');
      // 记录生成日期
      recordGenerationDate();
    } else {
      ElMessage.error('每日习题生成失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('每日习题生成失败：网络错误');
  }).finally(() => {
    // 无论成功失败，都清除生成状态
    setGeneratingStatus(false);
  });
}

onMounted(() => {
  // 只有在未生成过的情况下才触发生成
  if (!hasGeneratedToday()) {
    generateDailyPractice();
  }
  
  // 清理过期的生成状态（超过24小时的生成状态）
  const generatingStatusTimestamp = localStorage.getItem('generatingStatusTimestamp');
  if (generatingStatusTimestamp) {
    const now = new Date().getTime();
    const elapsed = now - parseInt(generatingStatusTimestamp);
    
    // 如果生成状态超过24小时，清除它
    if (elapsed > 24 * 60 * 60 * 1000) {
      localStorage.removeItem('generatingStatus');
      localStorage.removeItem('generatingStatusTimestamp');
    }
  }
});
</script>

<style scoped>
.student-dashboard {
  width: 100%;
  height: 100%;
  background-color: transparent;
  overflow: auto;
}
</style>