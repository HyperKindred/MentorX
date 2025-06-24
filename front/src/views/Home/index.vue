<template>
  <div class="background">
    <Birds/>
  </div>
  <div class="main">
    <h1>Welcome to MENTOR X</h1>
    <p>"Your AI Teaching Assistant for Practice and Evaluation."</p>
    <div class="logIn">
      <button class="logInBtn" @click="showLogIn = true">Sign in</button>
    </div>

    <div class="feature-display">
      <el-carousel :interval="5000" arrow="never">
        <el-carousel-item :key="1" class="slide-content-item">
          <h1>1</h1>
        </el-carousel-item>
        <el-carousel-item :key="2" class="slide-content-item">
          <h1>2</h1>
        </el-carousel-item>
        <el-carousel-item :key="3" class="slide-content-item">
          <h1>3</h1>
        </el-carousel-item>
        <el-carousel-item :key="4" class="slide-content-item">
          <h1>4</h1>
        </el-carousel-item>
        
      </el-carousel>
    </div>
  </div>
  <LogIn v-model:visible="showLogIn" @close-login="closeLogIn"/>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import LogIn from '../LogIn/index.vue'
import Birds from '../Background/Birds.vue'

const store = mainStore();
const router = useRouter();
const showLogIn = ref(false);

const closeLogIn = () => {
  showLogIn.value = false;
}
onMounted(() => {

});


</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

#app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
.main {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #1c3976ac;
    background-attachment: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    min-width: 100vw;
    margin: 0 auto;
    color: #f8f8f8;
}

.h1 {
    margin: 0.4rem;
    font-size: 1.2rem;
}

.p {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 100;
    margin: 1.2rem 0;
    letter-spacing: 0.1rem;
}

.logIn {
  margin-top: 4rem;
}

.logIn button {
  background-color: #417dff;
  color: #f8f8f8;
  padding: 0.4rem 1rem;
    border: 2px solid #fff;
    outline: none;
    cursor: pointer;
    width: 10rem;
    height: 3rem;
    border-radius: 8px;
    transition: all 100ms ease-in;
    margin: 0.6rem 0;
    font-size: 1.5rem;
    padding: 0.5rem 0;
}

.logIn button:hover{
  background-color: #417dffd8;

}

.logIn button:active{
  transform: scale(0.95 0.95);
}

.feature-display {
  width: 100%;
  height: 100%;
  margin-top: 5rem;
}

</style>