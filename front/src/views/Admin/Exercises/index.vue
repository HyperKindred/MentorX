<template>
  <div class="Main">
    <div class="exercise-list">
      <div class="exercise-item" v-for="item in exercises" :key="item.id">
        <div class="question-text" :title="item.content">{{ item.content }}</div>
        <div class="difficulty">难度等级：{{ item.difficulty }} </div>
        <div class="type">题型：{{ getTypeLabel(item.type) }} </div>
        <el-button @click="deleteExercise(item)">删除</el-button>
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
const chapter = ref<Record<string, any>>({});
const exercises = ref([]);

const typeMap: Record<string, string> = {
  choices: '选择题',
  blanks: '填空题',
  answers: '简答题'
};

const getTypeLabel = (type: string): string => {
  return typeMap[type] || '未知题型';
};

const getExercisesList = () => {
  const formData = new FormData();
  formData.append('id', chapter.value.id);

  axios.post(`${store.ip}/api/teacher/getExercisesList`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    const data = res.data;

    if (data.ret === 0 && Array.isArray(data.exercisesList)) {
      exercises.value = data.exercisesList;
    } else {
      exercises.value = []; 
      ElMessage.error('获取习题列表失败：' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取习题列表失败：网络错误');
  });
};

const deleteExercise = (exercise: any) => {
  const formData = new FormData();
  formData.append('id', exercise.id);
  axios.post(`${store.ip}/api/deleteExercise`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    ElMessage.success('删除成功');
    const data = res.data;
    if (data.ret === 0) {
      getExercisesList();
    } else {
      ElMessage.error('删除习题失败' + data.msg);
    }
  }).catch(() => {
    ElMessage.error('删除习题失败：网络错误');
  });
}

onMounted(() => {
  chapter.value = JSON.parse(localStorage.getItem('selectedChapter') || '{}');
  if (chapter.value?.id) {
    getExercisesList();
  }
});



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