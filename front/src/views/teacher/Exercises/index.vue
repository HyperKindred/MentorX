<template>
  <div class="Main">
    <div class="exercise-list">
      <div class="exercise-item" v-for="item in exercises" :key="item.id" @click="handleExerciseClick(item)">
        <div class="question-text" :title="item.content">{{ item.content }}</div>
        <div class="difficulty">难度等级：{{ item.difficulty }} </div>
        <div class="type">题型：{{ getTypeLabel(item.type) }} </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import T_exercise from '../Exercises/index.vue'
const store = mainStore();
const router = useRouter();
const chapter = ref<Record<string, any>>({});
const exercises = ref([]);
const selectedExercise = ref<any>(null);

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
  axios.post(`${store.ip}/api/getExercisesList`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  }).then(res => {
    if (res.data.ret === 0 && res.data.exercisesList?.exercise) {
      exercises.value = Array.isArray(res.data.exercisesList.exercise)
        ? res.data.exercisesList.exercise
        : [res.data.exercisesList.exercise];
    } else {
      ElMessage.error('获取习题列表失败：' + res.data.msg);
    }
  }).catch(() => {
    ElMessage.error('获取习题列表失败：网络错误');
  });
}

const handleExerciseClick = (item: any) => {
  selectedExercise.value = item;
  localStorage.setItem('selectedExercise', JSON.stringify(selectedExercise.value));
  store.addTab('习题', T_exercise);
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