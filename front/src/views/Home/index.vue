<template>
  <div class="main">
    <div class="scroll-container" :class="{ scrolled: isScrolled }">
      <!-- 欢迎屏幕 -->
      <div class="welcome-screen">
        <div class="logo">
          <svg class="robot-icon" viewBox="0 0 24 24">
            <path
              d="M20,9V7c0-1.1-0.9-2-2-2h-4c-0.6,0-1,0.4-1,1s0.4,1,1,1h4v2h-4c-0.6,0-1,0.4-1,1v4c0,0.6,0.4,1,1,1h4v2h-4 c-1.1,0-2-0.9-2-2v-1H8v1c0,1.1-0.9,2-2,2H4c-1.1,0-2-0.9-2-2v-4c0-1.1,0.9-2,2-2h4c1.1,0,2,0.9,2,2v1h8v-1c0-0.6-0.4-1-1-1H4V9 H20z M9,15c-0.6,0-1-0.4-1-1s0.4-1,1-1s1,0.4,1,1S9.6,15,9,15z M15,15c-0.6,0-1-0.4-1-1s0.4-1,1-1s1,0.4,1,1S15.6,15,15,15z" />
          </svg>
          <span>MENTOR X</span>
        </div>

        <h1 class="title">Welcome to MENTOR X</h1>
        <p class="title-content">"Your AI Teaching Assistant for Practice and Evaluation."</p>

        <div class="logIn">
          <button class="logInBtn" @click="showLogIn = true">Sign in</button>
        </div>

        <div class="scroll-hint" @click="scrollToFeatures">
          <svg class="arrow-icon" viewBox="0 0 24 24">
            <path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" />
          </svg>
        </div>
      </div>

      <!-- 功能展示区域 -->
      <div class="features-section">
        <div class="back-to-top-hint" @click="scrollToTop">
          <svg class="arrow-up-icon" viewBox="0 0 24 24">
            <path d="M7.41,15.41L12,10.83l4.59,4.58L18,14l-6-6l-6,6L7.41,15.41z" />
          </svg>
        </div>
        <div class="feature-display">
          <el-carousel :interval="5000" arrow="never" height="400px">
            <el-carousel-item :key="1" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">个性习题</h2>
                <p class="slide-description">AI智能生成个性化习题，量身定制学习内容，支持自主训练，充分激发学习主动性。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide1" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
            <el-carousel-item :key="2" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">AI问答</h2>
                <p class="slide-description">AI智能问答，实时辅导学生，解答疑难问题，扫清学习障碍。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide2" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
            <el-carousel-item :key="3" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">课件生成</h2>
                <p class="slide-description">根据章节内容智能生成课件，省时省力，助力教师高效备课。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide3" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
            <el-carousel-item :key="4" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">智能批改</h2>
                <p class="slide-description">智能批改学生作答，提供详细分析，高效准确评估学习情况，精准定位知识薄弱点。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide4" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
            <el-carousel-item :key="5" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">学习追踪</h2>
                <p class="slide-description">实时追踪学习进度，可视化分析各章节掌握情况，精准定位薄弱环节，助力重点突破。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide5" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
            <el-carousel-item :key="6" class="slide-content">
              <div class="slide-text">
                <h2 class="slide-title">信息统计</h2>
                <p class="slide-description">可视化统计系统各类信息，帮助管理者一目了然掌握全局，辅助科学决策。</p>
              </div>
                  <div class="media-container">
                    <video autoplay loop muted playsinline>
                      <source :src="slide6" type="video/mp4">
                    </video>
                  </div>
            </el-carousel-item>
          </el-carousel>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="brain-icon" viewBox="0 0 24 24">
                <path
                  d="M12,3C8.69,3,6,5.69,6,9c0,1.7,0.7,3.22,1.82,4.33C6.44,14.07,6,15.07,6,16.19C6,19.17,8.69,22,12,22s6-2.83,6-5.81 c0-1.12-0.44-2.12-1.82-2.86C17.3,12.22,18,10.7,18,9C18,5.69,15.31,3,12,3z M13,17c0,0.55-0.45,1-1,1s-1-0.45-1-1s0.45-1,1-1 S13,16.45,13,17z M16,14c-0.3,0.22-0.64,0.39-1,0.5c-0.03,1.49-1.17,2.5-3,2.5s-2.97-1.01-3-2.5c-0.36-0.11-0.7-0.28-1-0.5 c-0.03,1.49-1.17,2.5-3,2.5s-2.97-1.01-3-2.5c0-1.65,1.35-3,3-3c0.55,0,1,0.45,1,1s-0.45,1-1,1c-0.55,0-1,0.45-1,1 c0,0.55,0.45,1,1,1c0.55,0,1,0.45,1,1c0,0.55-0.45,1-1,1c-0.55,0-1,0.45-1,1c0,0.55,0.45,1,1,1c1.65,0,3-1.35,3-3 c0-0.55,0.45-1,1-1s1,0.45,1,1c0,1.65,1.35,3,3,3s3-1.35,3-3c0-0.55-0.45-1-1-1c-0.55,0-1-0.45-1-1c0-0.55,0.45-1,1-1 c0.55,0,1-0.45,1-1c0-0.55-0.45-1-1-1c-0.55,0-1-0.45-1-1c0-0.55,0.45-1,1-1c1.65,0,3,1.35,3,3C19,12.65,17.65,14,16,14z" />
              </svg>
            </div>
            <h3>AI驱动学习</h3>
            <p>根据学习进度和技能水平，量身定制自适应学习路径。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="chart-icon" viewBox="0 0 24 24">
                <path
                  d="M16,11V5h4v6H16z M10,7V5h4v2H10z M4,9V5h4v4H4z M16,19v-6h4v6H16z M10,13v-2h4v2H10z M4,19v-4h4v4H4z M10,19v-4h4v4H10z" />
              </svg>
            </div>
            <h3>进度追踪</h3>
            <p>详细追踪和分析学习进度，全面掌握知识熟练度。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="comments-icon" viewBox="0 0 24 24">
                <path
                  d="M20,2H4C2.9,2,2,2.9,2,4v18l4-4h14c1.1,0,2-0.9,2-2V4C22,2.9,21.1,2,20,2z M6,14v-2h12v2H6z M18,11H6V9h12V11z M18,8H6V6 h12V8z" />
              </svg>
            </div>
            <h3>智能教学</h3>
            <p>智能生成学习内容与习题，实时反馈，助力高效学习。</p>
          </div>
        </div>

        <div class="footer">
          © 2023 MENTOR X - 用AI改变教育
        </div>
      </div>
    </div>

    <div class="background">
      <!-- 动态小鸟背景 -->
      <div class="bird" v-for="(bird, index) in birds" :key="index" :style="bird.style"></div>
    </div>
  </div>
  <LogIn v-model:visible="showLogIn" @close-login="closeLogIn" />
</template>

<script lang="ts" setup>
import { defineComponent, ref, onMounted } from 'vue';
import { mainStore } from '../../store/index.ts';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import LogIn from '../LogIn/index.vue'
import Birds from '../Background/Birds.vue'
import slide1 from '../../assets/videos/生成习题.mp4'
import slide2 from '../../assets/videos/AI问答.mp4'
import slide3 from '../../assets/videos/课件生成.mp4'
import slide4 from '../../assets/videos/批改习题.mp4'
import slide5 from '../../assets/videos/学习情况.mp4'
import slide6 from '../../assets/videos/统计信息.mp4'
const store = mainStore();
const router = useRouter();
const showLogIn = ref(false);
const isScrolled = ref(false);
const birds = ref<Array<{ style: object }>>([]);

const createBirds = () => {
  const newBirds = [];
  for (let i = 0; i < 12; i++) {
    newBirds.push({
      style: {
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDuration: `${10 + Math.random() * 20}s`,
        animationDelay: `${Math.random() * 5}s`,
        opacity: `${0.2 + Math.random() * 0.5}`,
        width: `${20 + Math.random() * 30}px`,
        height: `${20 + Math.random() * 30}px`
      }
    });
  }
  birds.value = newBirds;
};



const scrollToFeatures = () => {
  isScrolled.value = true;
};

// 滚动到顶部
const scrollToTop = () => {
  isScrolled.value = false;
};
const closeLogIn = () => {
  showLogIn.value = false;
}
// 初始化页面
onMounted(() => {
  createBirds();
  showLogIn.value = false;
});


</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.main {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #0a1a3d, #1c3976);
  background-attachment: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  min-width: 100vw;
  overflow: hidden;
  line-height: 1.6;
  position: relative;
}

.scroll-container {
  position: relative;
  height: 100vh;
  overflow: hidden;
  width: 100%;
}

.welcome-screen {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  z-index: 20;
  transition: transform 1.2s cubic-bezier(0.33, 1, 0.68, 1);
  background: rgba(10, 26, 61, 0.92);
  backdrop-filter: blur(8px);
}

.scrolled .welcome-screen {
  transform: translateY(-100%);
}

.features-section {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  min-height: 100vh;
  padding: 2rem;
  transition: transform 1.2s cubic-bezier(0.33, 1, 0.68, 1);
  transform: translateY(0);
  margin-top: 1.8rem;
}

.scrolled .features-section {
  transform: translateY(-100%);
}

.logo {
  position: absolute;
  top: 30px;
  left: 30px;
  display: flex;
  align-items: center;
  font-size: 1.8rem;
  font-weight: 700;
  color: #5e9aff;
  z-index: 30;
  animation: fadeInDown 0.8s ease-out;
}

.robot-icon {
  width: 2.2rem;
  height: 2.2rem;
  margin-right: 10px;
  fill: currentColor;
}

.title {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  background: linear-gradient(to right, #ffffff, #a0c4ff);
  background-clip: text;
  color: transparent;
  animation: fadeInUp 0.8s ease-out;
}

.title-content {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  max-width: 600px;
  opacity: 0.9;
  font-weight: 300;
  padding: 0 20px;
  animation: fadeIn 1.2s ease-out 0.3s forwards;
  opacity: 0;
  color: #f8f8f8;
}

.logIn {
  margin-top: 2rem;
  animation: fadeIn 1.2s ease-out 0.6s forwards;
  opacity: 0;
}

.logInBtn {
  background: linear-gradient(45deg, #417dff, #5e9aff);
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  font-size: 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(65, 125, 255, 0.4);
  font-weight: 600;
}

.logInBtn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(65, 125, 255, 0.6);
}

.logInBtn:active {
  transform: translateY(1px);
}

.scroll-hint {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.8;
  animation: bounce 2s infinite;
  cursor: pointer;
  z-index: 30;
}

.scroll-hint:hover {
  opacity: 1;
}

.arrow-icon {
  width: 2.5rem;
  height: 2.5rem;
  fill: #5e9aff;
  transition: all 0.3s ease;
}

.scroll-hint:hover .arrow-icon {
  transform: scale(1.2);
  filter: drop-shadow(0 0 8px rgba(160, 196, 255, 0.7));
}

@keyframes bounce {

  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0) translateX(-50%);
  }

  40% {
    transform: translateY(-20px) translateX(-50%);
  }

  60% {
    transform: translateY(-10px) translateX(-50%);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-40px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.back-to-top-hint {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.8;
  animation: bounceReverse 2s infinite;
  cursor: pointer;
  z-index: 30;
  width: 50px;
  height: 50px;
}

.back-to-top-hint:hover {
  opacity: 1;
}

.back-to-top-hint .arrow-up-icon {
  width: 2.5rem;
  height: 2.5rem;
  fill: #5e9aff;
  transition: all 0.3s ease;
}

.back-to-top-hint:hover .arrow-up-icon {
  transform: scale(1.2);
  filter: drop-shadow(0 0 8px rgba(160, 196, 255, 0.7));
}

/* 反向弹跳动画 */
@keyframes bounceReverse {

  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0) translateX(-50%);
  }

  40% {
    transform: translateY(20px) translateX(-50%);
  }

  60% {
    transform: translateY(10px) translateX(-50%);
  }
}

.feature-display {
  width: 100%;
  max-width: 900px;
  margin: 80px auto 3rem;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.slide-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-right: 2rem;
}

.slide-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  min-height: 400px;
}

.slide-title {
  font-size: 2.2rem;
  margin-bottom: 1rem;
  color: #a0c4ff;
  font-weight: 700;
}

.slide-description {
  font-size: 1.2rem;
  max-width: 600px;
  margin-bottom: 1rem;
  line-height: 1.6;
  opacity: 0.9;
  text-align: center;
  color: #f8f8f8;
}

.media-container {
  width: 100%;
  max-width: 800px;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.4);
  background: #000;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-container img,
.media-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 0 auto 0;
  width: 100%;
  max-width: 1000px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.8rem 1.5rem;
  text-align: center;
  transition: all 0.4s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transform: translateY(30px);
  opacity: 0;
  color: #f8f8f8;
}

.scrolled .feature-card {
  transform: translateY(0);
  opacity: 1;
}

.feature-card:nth-child(1) {
  transition-delay: 0.1s;
}

.feature-card:nth-child(2) {
  transition-delay: 0.2s;
}

.feature-card:nth-child(3) {
  transition-delay: 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
  background: rgba(65, 125, 255, 0.15);
  box-shadow: 0 8px 25px rgba(65, 125, 255, 0.2);
}

.feature-icon {
  font-size: 3.5rem;
  margin-bottom: 1.2rem;
  color: #5e9aff;
  display: flex;
  justify-content: center;
}

.brain-icon,
.chart-icon,
.comments-icon {
  width: 3.5rem;
  height: 3.5rem;
  fill: currentColor;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.feature-card p {
  font-size: 1rem;
  margin-bottom: 0;
  opacity: 0.8;
}

.footer {
  padding: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  opacity: 0.7;
  width: 100%;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #f8f8f8;
}

.back-to-top {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 50px;
  height: 50px;
  background: rgba(65, 125, 255, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 100;
  opacity: 0;
  transition: all 0.3s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.back-to-top.show {
  opacity: 1;
}

.back-to-top:hover {
  transform: translateY(-3px);
  background: rgba(65, 125, 255, 1);
  box-shadow: 0 6px 15px rgba(65, 125, 255, 0.5);
}

.arrow-up-icon {
  width: 1.5rem;
  height: 1.5rem;
  fill: white;
}

.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.bird {
  position: absolute;
  width: 30px;
  height: 30px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="rgba(255,255,255,0.3)"><path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  animation: fly linear infinite;
}

@keyframes fly {
  0% {
    transform: translateX(-100px) translateY(0);
  }

  50% {
    transform: translateX(calc(100vw + 100px)) translateY(50px);
  }

  100% {
    transform: translateX(calc(100vw + 100px)) translateY(-50px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  /* ... 其他响应式样式保持不变 ... */

  .feature-display {
    margin-top: 60px;
    /* 移动端减少顶部间距 */
    min-height: auto;
    /* 移除固定高度 */
  }

  .slide-content {
    padding: 1.5rem;
    min-height: auto;
    /* 移除固定高度 */
  }

  .media-container {
    height: 200px;
    /* 减少移动端图片高度 */
  }

  .features-grid {
    padding: 0 1rem;
  }

  .feature-card {
    padding: 1.2rem;
    /* 减少内边距 */
    margin-bottom: 1rem;
    /* 增加卡片间距 */
  }

  .back-to-top-hint {
    top: 20px;
    /* 移动端调整位置 */
  }
}

@media (max-width: 480px) {
  /* ... 其他响应式样式保持不变 ... */

  .slide-title {
    font-size: 1.5rem;
    /* 减小标题字号 */
  }

  .slide-description {
    font-size: 0.9rem;
    /* 减小描述字号 */
    margin-bottom: 1.5rem;
  }

  .media-container {
    height: 150px;
    /* 进一步减少图片高度 */
  }

  .feature-icon {
    margin-bottom: 0.8rem;
  }

  .feature-card h3 {
    font-size: 1.2rem;
    /* 减小卡片标题字号 */
  }

  .feature-card p {
    font-size: 0.85rem;
    /* 减小卡片描述字号 */
  }

  .back-to-top-hint {
    width: 40px;
    height: 40px;
    top: 15px;
  }

  .back-to-top-hint .arrow-up-icon {
    width: 2rem;
    height: 2rem;
  }
}
</style>