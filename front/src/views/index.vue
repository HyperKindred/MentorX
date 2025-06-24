<template>
  <div class="tab-container">
    <div class="tab-header-bar">
      <el-dropdown trigger="click" @command="handleDropdownCommand">
        <el-avatar shape="square" :size="40" :src="getUserAvatar()" fit="cover" style="cursor: pointer" />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="information">个人信息</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'S'" command="courses">我的课程</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="users">用户管理</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="learningInfo">学习情况</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="stats">统计信息</el-dropdown-item>
            <el-dropdown-item command="logout">登出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>


      <div class="username">{{ store.name }}</div>

      <el-tabs v-model="store.activeTab" type="card" @tab-remove="store.removeTab" @tab-click="onTabClick"
        class="tab-header">
        <el-tab-pane v-for="tab in store.tabs" :key="tab.name" :label="tab.title" :name="tab.name"
          :closable="tab.closable !== false" />
      </el-tabs>
    </div>
    <div class="tab-content">
      <component :is="getCurrentComponent()" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import TeacherImg from '../assets/images/Teacher.jpg';
import StudentImg from '../assets/images/Student.jpg';
import ManagerImg from '../assets/images/Manager.jpg';
import information from './Infomation/index.vue'
import A_user from './Admin/Users/index.vue'
import A_stats from './Admin/Statistic/index.vue'
import A_learningInfo from './Admin/LearningState/index.vue'
import S_myCourse from './Student/MyCourses/index.vue'
const store = mainStore();
const router = useRouter();
const activeTab = ref('home');
const tabIndex = ref(1);
const loginTime = parseInt(localStorage.getItem('loginTime') || '0', 10);
const logoutTime = Date.now();
const handleDropdownCommand = (command: string) => {
  switch (command) {
    case 'information':
      store.addTab('个人信息', information);
      break;
    case 'courses':
      store.addTab('我的课程', S_myCourse);
      break;
    case 'users':
      store.addTab('用户管理', A_user);
      break;
    case 'learningInfo':
      store.addTab('学习情况', A_learningInfo);
      break;
    case 'stats':
      store.addTab('统计信息', A_stats);
      break;
    case 'logout':
      if (loginTime) {
        const durationMs = logoutTime - loginTime;
          const formData = new FormData();
          formData.append('time', durationMs/1000);
          axios({
            method: 'post',
            url: `${store.ip}/api/sumTime`,
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
            data: formData,
          })
            .then((response) => {
              const res = response.data;
              if (res.ret === 0) {
                alert(formData.time);
              } else {
                ElMessage.error('上传时间数据失败：' + res.msg);
              }
            })
            .catch(() => {
              ElMessage.error('上传时间数据失败，请稍后重试！');
            });
        };
      
      localStorage.clear();
      store.tabs = [
        { name: 'home', title: '首页', component: Home, closable: false }
      ],
        store.getUserInfo();
      router.push({ path: '/Main' })
      break;
  }
};

// 获取用户头像
const getUserAvatar = () => {
  switch (store.type) {
    case 'S':
      return StudentImg;
    case 'T':
      return TeacherImg;
    case 'A':
      return ManagerImg;
  }
};

function getCurrentComponent() {
  const tab = store.tabs.find(t => t.name === store.activeTab);
  return tab ? tab.component : null;
}

function onTabClick(tab: any) {
  activeTab.value = tab.name;
}

onMounted(() => {
  store.getUserInfo();
});


</script>

<style scoped>
.tab-container {
  display: flex;
  flex-direction: column;
  left: 0%;
  top: 0%;
  position: absolute;
  width: 100vw;
  height: 98.5vh;
  overflow: hidden;
}

.tab-header {
  flex: 1;
  margin-left: 0.5rem;
  margin-top: 1rem;
}


.tab-content {
  flex-grow: 1;
  overflow: auto;
  padding: 16px;
  background: #f5f5f5;
}

.username {
  margin-left: 0.5rem;
  color: #080808;
  letter-spacing: 0.1rem;
}


.tab-header-bar {
  display: flex;
  align-items: center;
  padding: 0 16px;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #eee;
}
</style>
