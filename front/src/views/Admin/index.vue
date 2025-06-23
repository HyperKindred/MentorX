<template>
  <div class="main">
    <el-row :gutter="20" class="course-row">
      <el-col v-for="item in courses" :key="item.id" :span="6" class="course-col">
        <el-card :body-style="{ padding: '10px' }" shadow="hover" @click="handleCardClick(item.id, item.name)"
          style="cursor: pointer;">
          <div class="course-info">
            <h3>{{ item.name }}</h3>
            <p>教师：{{ item.teacher_name }}</p>
            <p>学生人数：{{ item.student_num }}</p>
          </div>
          <el-button type="primary" @click="deleteCourse(item.id)">删除</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import A_chapter from './Chapter/index.vue'
const store = mainStore();
const courses = ref([]);

onMounted(() => {
  getCourseList();
});

const getCourseList = () => {
  axios({
    method: 'get',
    url: `${store.ip}/api/getCourseList`,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 0 && Array.isArray(responseData.courseList)) {
        if (Array.isArray(responseData.courseList)) {
          courses.value = responseData.courseList;
        }
        else {
          courses.value = [];
        }
      } else {
        ElMessage({
          message: '获取课程列表失败：' + responseData.msg,
          type: 'error',
        });
      }
    })
    .catch((error) => {
      console.error('Error posting data:', error);
      ElMessage({
        message: '获取课程列表失败：网络错误，请稍后重试！',
        type: 'error',
        duration: 5000,
        grouping: true,
      });
    });
};

const deleteCourse = (id: number) => {
  const formData = new FormData();
  formData.append('id', id)
  axios({
    method: 'post',
    url: `${store.ip}/api/deleteCourse`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('删除课程成功！');
        getCourseList();
      } else {
        ElMessage.error('删除课程失败：' + res.msg);
      }
    })
    .catch(() => {
      ElMessage.error('请求失败，请稍后重试！');
    });
}

const handleCardClick = (id: number, name: string) => {
  localStorage.setItem('selectedCourseId', id.toString());
  store.addTab(name, A_chapter);
};


</script>

<style scoped></style>
