<template>
  <div class="Main">
    <el-row :gutter="20" class="course-row">
      <el-col
        v-for="item in courses"
        :key="item.id"
        :span="6"
        class="course-col"
      >
        <el-card :body-style="{ padding: '10px' }" shadow="hover">
          <img :src="courseImg" class="course-img" />
          <div class="course-info">
            <h3>{{ item.name }}</h3>
            <p>教师：{{ item.teacher_name }}</p>
            <p>学生人数：{{ item.student_num }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import courseImg from '../../assets/images/course.png'
const store = mainStore();
const router = useRouter();
const courses = ref([]);


onMounted(() => {
    getCourseList();
});


const getCourseList = () => {
  axios({
    method: 'get',
    url: `${store.ip}/api/getCourseList`,
    headers: {
      Authorization: localStorage.getItem('token'),
    },
  })
    .then((response) => {
      const responseData = response.data;
      if (responseData.ret === 0 && Array.isArray(responseData.courseList)) {
        courses.value = responseData.courseList;
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


</script>

<style scoped>
.Main {
  left: 0%;
  top: 0%;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(135, 206, 250, 0.254);
  padding: 20px;
}

.course-row {
  display: flex;
  flex-wrap: wrap;
}

.course-col {
  margin-bottom: 20px;
}

.course-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.course-info {
  margin-top: 10px;
}
</style>
