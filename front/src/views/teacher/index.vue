<template>
  <div class="Main">
    <el-button type="primary" @click="dialogVisible = true">新建课程</el-button>
    <el-dialog v-model="dialogVisible" title="新建课程" width="30%">
      <el-input
        v-model="Cname"
        placeholder="请输入课程名称"
        clearable
      ></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddCourse">新建</el-button>
        </span>
      </template>
    </el-dialog>
    <el-row :gutter="20" class="course-row">
      <el-col
        v-for="item in courses"
        :key="item.id"
        :span="6"
        class="course-col"
      >
          <el-card
            :body-style="{ padding: '10px' }"
            shadow="hover"
            @click="handleCardClick(item.id, item.name)"
            style="cursor: pointer;"
          >
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
import T_chapter from './Chapter/index.vue';

const store = mainStore();
const router = useRouter();
const courses = ref([]);
const Cname = ref('');
const dialogVisible = ref(false);
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

const handleAddCourse = () => {
  if (!Cname.value.trim()) {
    ElMessage.warning('请输入课程名称');
    return;
  }
  const formData = new FormData();
  formData.append('name', Cname.value)

  axios({
    method: 'post',
    url: `${store.ip}/api/teacher/addCourse`,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    data: formData,
  })
    .then((response) => {
      const res = response.data;
      if (res.ret === 0) {
        ElMessage.success('新建课程成功！');
        Cname.value = '';
        getCourseList();
        dialogVisible.value = false;
      } else {
        ElMessage.error('新建课程失败：' + res.msg);
      }
    })
    .catch(() => {
      ElMessage.error('请求失败，请稍后重试！');
    });
};

const handleCardClick = (id: number, name:string) => {
  localStorage.setItem('selectedCourseId', id.toString());
  store.addTab(name, T_chapter);
};


</script>

<style scoped>

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
