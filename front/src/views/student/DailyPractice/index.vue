<template>
    <div class="main">
        <div class="left-panel">
            <div class="left-title">往日习题</div>
            <div class="practice-list">
                <div v-for="practice in practices" :key="practice.id" class="practice-item" :class="{active: activePractice === practice.id}" @click="selectPractice(practice)">
                    <span class="practice-date">{{ practice.date }}</span>
                </div>
            </div>
            <div class="practice-calendar">

            </div>
        </div>
        <div class="right-panel">
            <div class="right-title">每日一题</div>
            <div class="content-area">
                <div class="practice-content">

                </div>
                <div class="answer-section">

                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { mainStore } from '../../../store/index.ts';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { active } from 'sortablejs';
const store = mainStore();
const practices = ref([]);
const activePractice = ref('');
const selectPractice = (practice: any) => {
  activePractice.value = practice.id;
};
</script>
<style scoped>
.main {
  display: flex;
  height: 100%;
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}

.left-panel {
  width: 300px;
  background: var(--backgroundColor2);
  border-right: 1.5px solid transparent;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.left-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--titleColor);
  margin: 0;
  padding: 20px 20px 28px 20px;
}

.practice-list {
  padding-bottom: 20px;
  padding-left: 5px;
  padding-right: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
}

.practice-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  border-radius: 5px;
  background-color: transparent;
  color: var(--textColor2);
  width: 270px;
}

.practice-item:hover {
  background-color: var(--backgroundColor2);
  color: var(--titleColor);
}

.practice-item.active {
  background-color: transparent;
  color: var(--titleColor);
  background-color: var(--backgroundColor2);
  font-weight: 540;
}

.practice-date{
  font-size: 14px;
  line-height: 1.4;
  flex: 1;
}

.practice-calendar {
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.right-title {
  color: var(--titleColor);
  padding: 1rem;
  text-align: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 800;
}

</style>