<template>
  
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
const store = mainStore();
const router = useRouter();
const chapter = ref([]);
const exercises = ref([]);

onMounted(() => {
  chapter = JSON.parse(localStorage.getItem('selectedChapter') || '{}');
});

const getExercisesList = () => {
  const formData = new FormData();
  formData.append('id', chapter.value.id);
  axios.post(`${store.ip}/api/getExercisesList`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: localStorage.getItem('token'),
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

</script>

<style scoped>
.Main {
  left: 0%;
  top: 0%;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: rgba(135, 206, 250, 0.254);
}

</style>