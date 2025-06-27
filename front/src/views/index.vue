<template>
  <div class="background">
    <Waves></Waves>
  </div>
  <div class="tab-container">
    <div class="tab-header-bar">
      <div class="head-left">
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
      <div class="head-right">
        <el-switch
          v-model="isDarkTheme"
          inline-prompt
          :active-icon="Moon"
          :inactive-icon="Sunny"
          active-text="夜间"
          inactive-text="日间"
          @change="toggleTheme"
          style="--el-switch-on-color: #417dff; --el-switch-off-color: #417dff; width: 4rem;"
        />
      </div>
    </div>
    <div class="tab-content">
      <keep-alive>
        <component 
          v-for="tab in store.tabs" 
          v-show="tab.name === store.activeTab"
          :key="tab.name"
          :is="tab.component" 
          v-bind="tab.props || {}" 
        />
      </keep-alive>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Sunny, Moon } from '@element-plus/icons-vue';
import TeacherImg from '../assets/images/Teacher.jpg';
import StudentImg from '../assets/images/Student.jpg';
import ManagerImg from '../assets/images/Manager.jpg';
import information from './Infomation/index.vue'
import A_user from './Admin/Users/index.vue'
import A_stats from './Admin/Statistic/index.vue'
import A_learningInfo from './Admin/LearningState/index.vue'
import S_myCourse from './Student/MyCourses/index.vue'
import Home from './Home/index.vue';
import Waves from './Background/Wave.vue'
const store = mainStore();
const router = useRouter();
const activeTab = ref('home');
const tabIndex = ref(1);
const isDarkTheme = ref(localStorage.getItem('theme') === 'dark'); 
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
        const durationS = logoutTime - loginTime;
        const durationInt = Math.trunc(durationS); 
          const formData = new FormData();
          formData.append('time', durationS);
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

              } else {
                ElMessage.error('上传时间数据失败：' + res.msg);
              }
            })
            .catch(() => {
              ElMessage.error('上传时间数据失败，请稍后重试！');
            });
        };
      store.tabs = [{ name: 'home', title: '首页', component: Home, closable: false }];
      store.activeTab= 'home';
      localStorage.clear();
      store.getUserInfo();
      router.push({ path: '/Main' })
      break;
  }
};

const toggleTheme = () => {
  const theme = isDarkTheme.value ? 'dark' : 'light';
  document.documentElement.setAttribute('theme', theme);
  localStorage.setItem('theme', theme);
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



function onTabClick(tab: any) {
  activeTab.value = tab.name;
}

onMounted(() => {
  store.getUserInfo();
  const savedTheme = localStorage.getItem('theme') || 'light';
  isDarkTheme.value = savedTheme === 'dark';
  document.documentElement.setAttribute('theme', savedTheme);
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
  right: 0px;
  bottom: 0px;

}

.tab-header {
  flex: none;
  margin-left: 2rem;
  margin-top: 1.6rem;
  border: none;

}

.tab-header :deep(.el-tabs__item) {
    background-color: white;
    height: 3rem;
    color: #417dff6e;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    border-right: 1px solid #417dff;
}

.tab-header :deep(.el-tabs__item.is-active) {
    color: #417dff;
}


.tab-header :deep(.el-tabs__nav) {
  border: none !important;
}

.tab-content {
  flex-grow: 1;
  overflow: auto;
  padding: 16px;
  background-color: var(--backgroundColor);
}

.username {
  margin-left: 0.5rem;
  color: #ffffff;
  letter-spacing: 0.1rem;
}


.tab-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 60px;
  background-color: #417dff;
  font-family: Arial, Helvetica, sans-serif;
}

.el-dropdown-menu {
  background-color: #417dff;
  color: white;
}

.el-dropdown-menu :deep(.el-dropdown-menu__item) {
  background-color: #417dff;
  color: white;
}

.el-dropdown-menu :deep(.el-dropdown-menu__item:hover) {
  background-color: #729fff;
  color: white;
}

.head-left {
  display: flex;
  align-items: center;
}

.head-right {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}
</style>
