<template>
  <div class="tab-container">
    <div class="tab-header-bar">
    <el-avatar @click="showSignIn = true" shape="square" :size="40" :src="logIn" alt="logIn" fit="cover" />
    <el-tabs v-model="store.activeTab" type='card' @tab-remove="store.removeTab" @tab-click="onTabClick" class="tab-header">
        <el-tab-pane
          v-for="tab in store.tabs"
          :key="tab.name"
          :label="tab.title"
          :name="tab.name"
          :closable="tab.closable !== false"
        />  
    </el-tabs>
    <el-button size="small" @click="store.addTab('新页面', Home)">+ 添加页面</el-button>
    </div>
    <!-- 内容区域 -->
    <div class="tab-content">
      <component :is="getCurrentComponent()" />
    </div>
    <SignIn v-model:visible="showSignIn" @switch-to-signup="handleSwitchToSignUp" />
    <SignUp v-model:visible="showSignUp" @switch-to-signin="handleSwitchToSignIn" />
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import misakaImg from '../assets/images/Misaka Mikoto.jpg';
import logIn from '../assets/images/logIn.png';

import SignIn from './SignIn/index.vue'
import SignUp from './SignUp/index.vue'
const store = mainStore();
const router = useRouter();
const message = ref('');
const activeTab = ref('home');
const showSignIn = ref(false);
const showSignUp = ref(false);
const tabIndex = ref(1);






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

onMounted(() => {

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