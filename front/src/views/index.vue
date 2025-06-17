<template>
  <div class="tab-container">
    <div class="tab-header-bar">
    <el-avatar @click="showSignIn = true" shape="square" :size="40" :src="logIn" alt="logIn" fit="cover" />
    <el-tabs v-model="activeTab" class="tab-header">
      <el-tab-pane label="首页" name="home" />
    </el-tabs>
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
import Home from './Home/index.vue';
import SignIn from './SignIn/index.vue'
import SignUp from './SignUp/index.vue'
const store = mainStore();
const router = useRouter();
const message = ref('');
const activeTab = ref('home');
const showSignIn = ref(false);
const showSignUp = ref(false);


function getCurrentComponent() {
  switch (activeTab.value) {
    case 'home':
      return Home;
    default:
      return Home;
  }
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