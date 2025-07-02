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
  overflow: auto;
}
</style>