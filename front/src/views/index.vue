<template>
  <div class="background">
    <Waves></Waves>
  </div>
  <div class="tab-container">
    <div class="tab-header-bar">
      <div class="head-left">
        <div class="head-left-info">
      <el-dropdown trigger="click" @command="handleDropdownCommand">
        <el-avatar shape="square" :size="40" :src="getUserAvatar()" fit="cover" style="cursor: pointer" class="avatar" />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="information">个人信息</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'S'" command="courses">我的课程</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'S'" command="daily">每日练习</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="users">用户管理</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="learningInfo">学习情况</el-dropdown-item>
            <el-dropdown-item v-if="store.type === 'A'" command="stats">统计信息</el-dropdown-item>
            <el-dropdown-item command="logout">登出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <div class="username">{{ store.name }}</div>
      </div>
      </div>
      <div class="tab-container-flex">
        <el-tabs v-model="store.activeTab" type="card" @tab-remove="store.removeTab" @tab-click="onTabClick"
          class="tab-header">
          <el-tab-pane v-for="tab in store.tabs" :key="tab.name" :name="tab.name"
            :closable="false" class="fixed-width-tab">
            <template #label>
              <div class="tab-label-wrapper">
                <span class="tab-title" :title="tab.title">{{ tab.title }}</span>
                <el-icon 
                  v-if="tab.closable !== false" 
                  class="tab-close-btn" 
                  @click.stop="store.removeTab(tab.name)"
                >
                  <Close />
                </el-icon>
              </div>
            </template>
          </el-tab-pane>
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
import { ref, onMounted, nextTick } from 'vue';
import { mainStore } from '../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Sunny, Moon, Close } from '@element-plus/icons-vue';
import TeacherImg from '../assets/images/Teacher.jpg';
import StudentImg from '../assets/images/Student.jpg';
import ManagerImg from '../assets/images/Manager.jpg';
import information from './Infomation/index.vue'
import A_user from './Admin/Users/index.vue'
import A_stats from './Admin/Statistic/index.vue'
import A_learningInfo from './Admin/LearningState/index.vue'
import S_myCourse from './Student/MyCourses/index.vue'
import S_dailyPractice from './Student/DailyPractice/index.vue'
import Home from './Home/index.vue';
import Waves from './Background/Wave.vue'
import Sortable from 'sortablejs';
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
    case 'daily':
      store.addTab('每日练习',S_dailyPractice);
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

/**
 * 初始化拖拽排序功能
 */
const initSortable = () => {
  nextTick(() => {
    const tabNav = document.querySelector('.tab-header .el-tabs__nav');
    if (tabNav) {
      Sortable.create(tabNav as HTMLElement, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',
        filter: '.el-tabs__item[data-name="home"]', // 过滤首页标签，不允许拖拽
        preventOnFilter: false,
        onEnd: (evt) => {
          const { oldIndex, newIndex } = evt;
          if (oldIndex !== undefined && newIndex !== undefined && oldIndex !== newIndex) {
            // 使用store中的方法重新排序
            store.reorderTabs(oldIndex, newIndex);
          }
        }
      });
    }
  });
};

onMounted(() => {
  store.getUserInfo();
  const savedTheme = localStorage.getItem('theme') || 'light';
  isDarkTheme.value = savedTheme === 'dark';
  document.documentElement.setAttribute('theme', savedTheme);
  
  // 初始化拖拽排序
  initSortable();
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
  height: 100vh;
  overflow: hidden;
  right: 0px;
  bottom: 0px;

}

.avatar {
  margin-bottom: 6px;
}

.tab-content {
  flex: 1;
  overflow: auto;
  padding: 16px;
  background-color: var(--backgroundColor);
}

.username {
  margin-left: 0.5rem;
  color: #ffffff;
  letter-spacing: 0.1rem;
  margin-bottom: 3px;
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

.head-left-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-top: 1rem;
}

/* 标签页容器flex布局 */
.tab-container-flex {
  flex: 1;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.tab-header {
  flex: none;
  border: none;
  width: 100%;
  height: 100%;
}

.tab-header :deep(.el-tabs__item) {
    background-color: white;
    height: 3rem;
    color: #417dff6e;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    border-right: 1px solid #417dff;
    border-bottom: none;
}

.tab-header :deep(.el-tabs__content) {
  display: none;
}

.tab-header :deep(.el-tabs__header) {
  width: 100%;
  height: 100%;
  margin-bottom: 0;
  border-bottom: none;
}

.tab-header :deep(.el-tabs__nav-wrap) {
  width: 100%;
  height: 100%;
  margin-bottom: 0;
}

.tab-header :deep(.el-tabs__nav-scroll) {
  width: 100%;
  height: 100%;
}

.tab-header :deep(.el-tabs__item.is-active) {
  color: #417dff;
}


.tab-header :deep(.el-tabs__nav) {
  border: none;
  height: 100%;
  align-items: flex-end;
}

/* 自适应宽度标签页样式 - 使用deep穿透 */
.tab-header :deep(.el-tabs__nav) {
  display: flex;
  width: 100%;
}

.tab-header :deep(.el-tabs__item) {
  position: relative;
  flex: 1;
  max-width: 180px;
  overflow: hidden;
}

/* 隐藏默认关闭按钮 */
.tab-header :deep(.el-tabs__item .el-tabs__item__close) {
  display: none;
}

/* 自定义标签包装器样式 */
.tab-label-wrapper {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  box-sizing: border-box;
}

/* 标签页标题样式 */
.tab-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: auto;
  font-size: 14px;
  text-align: left;
}

/* 自定义关闭按钮样式 */
.tab-close-btn {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 1;
  transition: all 0.2s ease;
  background-color: transparent;
}

.tab-close-btn:hover {
  background-color: #b6c4e1;
  color: white;
}

/* 拖拽相关样式 */
.sortable-ghost {
  opacity: 0.5;
}

.sortable-chosen {
  background-color: var(--backgroundColor2);
}

.sortable-drag {
  background-color: var(--backgroundColor2);
  transform: rotate(5deg);
}

/* 确保首页标签不可拖拽的视觉提示 */
.el-tabs__item[data-name="home"] {
  cursor: default;
}

.el-tabs__item:not([data-name="home"]) {
  cursor: move;
}


</style>
