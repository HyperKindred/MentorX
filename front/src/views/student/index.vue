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
const practices = ref([]);
const generationDate = ref('');
// 获取今日日期字符串 (YYYY-MM-DD)
const getTodayDate = () => {
  const today = new Date();
  return today.toISOString().split('T')[0];
};

// 检查今日是否已生成习题
const hasGeneratedToday = () => {
  return generationDate.value === getTodayDate();
};

// 设置生成状态
const setGeneratingStatus = (status: boolean) => {
  localStorage.setItem('generatingStatus', status.toString());
  if (status) {
    localStorage.setItem('generatingStatusTimestamp', Date.now().toString());
  }
};

// 获取生成状态
const getGeneratingStatus = (): boolean => {
  return localStorage.getItem('generatingStatus') === 'true';
};

const getPracticeList = () => {
  const token = localStorage.getItem('token');
  axios.get(`${store.ip}/api/student/getDailyPracticeList`, {
    headers: { 'Authorization': `Bearer ${token}` }
  }).then(res => {
    const data = res.data;
    if (data.ret === 0) {
      const list = Array.isArray(data.exercisesList) ? data.exercisesList : [data.exercisesList];
      console.log('返回数据：', data);
      // 过滤无效项并排序
      practices.value = list
        .filter(p => p && p.date && p.exercise_id) // 确保必要字段存在
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      
      if (practices.value.length > 0) {
        generationDate.value = practices.value[0].date;
      }
    } else {
      practices.value = [];
      ElMessage.error('获取练习列表失败：' + data.msg);
    }
  }).catch(err => {
    console.error('请求失败', err);
    practices.value = []; // 确保设置为空数组
  });
};

// 生成每日习题
const generateDailyPractice = () => {
  // 设置生成状态
  setGeneratingStatus(true);
  console.log('正在生成习题');
  const token = localStorage.getItem('token');
  axios.get(`${store.ip}/api/student/generateDailyPractice`,{
    headers: {
      'Authorization': `Bearer ${token}`,
    }
  }).then(res => {
    const data = res.data;
    if (data.ret === 0) {
      ElMessage.success('每日习题已生成！');
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
  getPracticeList();
  setTimeout(() => {
    if (!hasGeneratedToday() && !getGeneratingStatus()) {
      generateDailyPractice();
    }
  }, 2000);
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