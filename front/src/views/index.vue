<template>
  <div class="tab-container">
    <div class="tab-header-bar">
      <!-- 登录前头像 -->
      <template v-if="store.type === 'U'">
        <el-avatar
          shape="square"
          :size="40"
          :src="logIn"
          alt="logIn"
          fit="cover"
          @click="showSignIn = true"
          style="cursor: pointer"
        />
      </template>

      <!-- 登录后头像 -->
      <template v-else>
        <el-dropdown trigger="click" @command="handleDropdownCommand">
          <el-avatar
            shape="square"
            :size="40"
            :src="getUserAvatar()"
            fit="cover"
            style="cursor: pointer"
          />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="store.type === 'S'" command="S_info">个人信息</el-dropdown-item>
              <el-dropdown-item v-if="store.type === 'S'" command="courses">我的课程</el-dropdown-item>
              <el-dropdown-item v-if="store.type === 'T'" command="T_info">个人信息</el-dropdown-item>
              <el-dropdown-item v-if="store.type === 'M'" command="M_info">个人信息</el-dropdown-item>
              <el-dropdown-item command="logout">登出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>

      <div class="username">{{ store.name }}</div>

      <el-tabs
        v-model="store.activeTab"
        type="card"
        @tab-remove="store.removeTab"
        @tab-click="onTabClick"
        class="tab-header"
      >
        <el-tab-pane
          v-for="tab in store.tabs"
          :key="tab.name"
          :label="tab.title"
          :name="tab.name"
          :closable="tab.closable !== false"
        />
      </el-tabs>
    </div>
    <div class="tab-content">
      <component :is="getCurrentComponent()" />
    </div>
    <SignIn v-model:visible="showSignIn" @switch-to-signup="handleSwitchToSignUp" @close-signin="closeSignIn"/>
    <SignUp v-model:visible="showSignUp" @switch-to-signin="handleSwitchToSignIn" @close-signup="closeSignUp"/>
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
import logIn from '../assets/images/logIn.png';

import SignIn from './SignIn/index.vue'
import SignUp from './SignUp/index.vue'
import T_info from './Teacher/Infomation/index.vue'
const store = mainStore();
const router = useRouter();
const message = ref('');
const activeTab = ref('home');
const showSignIn = ref(false);
const showSignUp = ref(false);
const tabIndex = ref(1);

const handleDropdownCommand = (command: string) => {
  switch (command) {
    case 'S_info':
      break;
    case 'T_info':
      store.addTab('个人信息', T_info);
      break;
    case 'M_info':
      break;
    case 'courses':
      break;
    case 'logout':
      localStorage.clear();
      store.getUserInfo();
      location.reload();
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
    case 'M':
      return ManagerImg;
    default:
      return logIn;
  }
};

function getCurrentComponent() {
  const tab = store.tabs.find(t => t.name === store.activeTab);
  return tab ? tab.component : null;
}



function onTabClick(tab: any) {
  activeTab.value = tab.name;
}

const handleSwitchToSignUp = () => {
  showSignIn.value = false;
  showSignUp.value = true;
};

const handleSwitchToSignIn = () => {
  showSignUp.value = false;
  showSignIn.value = true;
};

const closeSignUp = () => {
  showSignUp.value = false;
}

const closeSignIn = () => {
  showSignIn.value = false;
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
    top:0%;
    position: absolute;
    width: 100vw;
    height: 98.5vh;
    overflow: hidden;
}
.tab-header {
  flex: 1;
  margin-left: 16px;
}
.tab-content {
  flex-grow: 1;
  overflow: auto;
  padding: 16px;
  background: #f5f5f5;
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